import transformers as t
from PIL import Image
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mb_utils.src import logging
from pp_weight_estimation.utils.slack_connect import send_message_to_slack
from pp_weight_estimation.core.get_weight import get_seg, get_final_mask, get_final_img, get_histogram, get_val, split_filename, get_final_mask_filter
from pp_weight_estimation.core.s3_io import  download_image
from pp_weight_estimation.core.gpt_support import get_count
from typing import List,Dict,Union
import yaml
import boto3
from datetime import datetime

logger = logging.logger 
#model_checkpoint = '/Users/test/test1/mit-segformer-s' 
#model = t.TFSegformerForSemanticSegmentation.from_pretrained(model_checkpoint)

__all__ = ["load_color_values", "process_pipeline"]

def load_config(yaml_path: str) -> dict:
    """
    Function to load configurations from a YAML file
    Args:
        yaml_path (str): Path to the YAML file
    Returns:
        dict: Dictionary containing configurations
    """
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_color_values_old(csv_path : str, logger: logging.Logger = None) -> Dict:
    """
    Function to load color values from a CSV file
    Args:
        csv_path (str): Path to the CSV file
        logger (Logger): Logger object
    Returns:
        dict: Dictionary containing color values
    """
    if logger:
        logger.info("Loading color values from CSV")
    color_dict = {}
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        taxcode = row['taxonomy_code']
        site = row['site_id']
        color = row['colors']
        if taxcode and site and color:
            composed_key = f"{site}_{taxcode}"
            color_list = eval(color)
            color_dict[composed_key] = color_list
    return color_dict

def load_color_values(csv_path : str, logger: logging.Logger = None) -> Dict:
    """
    Function to load color values from a CSV file
    Args:
        csv_path (str): Path to the CSV file
        logger (Logger): Logger object
    Returns:
        dict: Dictionary containing color values
    """
    if logger:
        logger.info("Loading color values from CSV")
    color_dict = {}
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        item_code = row['item_code']
        model_version = row['model_version']
        #site = row['site_id']
        color = row['colors']
        # if taxcode and site and color:
        #     composed_key = f"{site}_{taxcode}"
        #     color_list = eval(color)
        #     color_dict[composed_key] = color_list
        if item_code and model_version and pd.isna(color) is False:
            composed_key = f"{item_code}_{model_version}"
            color_list = eval(color)
            color_dict[composed_key] = color_list
        else:
            composed_key = f"{item_code}_{model_version}"
            color_dict[composed_key] = None
    return color_dict

def process_pipeline(config_path: str, logger: logging.Logger = None, **kwargs) -> Union[pd.DataFrame, List]:
    """
    Function to process the pipeline of Production Planning.
    
    This function automates the process of downloading images from an S3 bucket, applying segmentation and masking,
    calculating histograms, and saving the results to an output CSV file. The function uses configurations provided
    in a YAML file for flexibility.

    Args:
        config_path (str): Path to the YAML configuration file.
        logger (logging.Logger): Logger object for logging messages (optional).
        **kwargs: Additional keyword arguments (optional).
        
    Returns:
        tuple: A tuple containing:
            - str: The path to the output CSV file.
            - list: A list of results for each processed image.
    """
    config = load_config(config_path)

    input_csv_path = config['data']['input_csv_path']
    #reference_file = config['data']['gt_csv_path']
    val_color_csv_path = config['data']['val_color_csv_path']
    # logger = config['data']['logger']
    # if logger:
    #     logger = logging.logger

    replace_images = config['data'].get('replace_images', False)
    path_to_save_images = config['data']['path_to_save_images']
    if path_to_save_images[-1] != '/':
        path_to_save_images += '/'
    
    save_plots = config['results'].get('save_plots', False)
    final_mask_vals = config['results'].get('final_mask_vals', 50)
    mask_model_val = config['results'].get('model_val', 0.08)
    mask_val = config['results'].get('mask_val', 0.3)
    new_bg_removal = config['results'].get('background_removal', True)
    equalizer_items = config['results'].get('equalizer_items')
    slack_post = config['results'].get('slack_post', False)
    slack_webhook = config['results'].get('slack_webhook', None)

    model_path = config['model']['model_path']
    model_name = config['model']['model_name']
    model_version = config['model']['model_version']

    bucket = config['aws_data']['bucket_name']
    profile = config['aws_data']['profile']

    gpt_response = config['gpt_res'].get('gpt_response', False)
    gpt_token = config['gpt_res'].get('gpt_token', None)
    gpt_model = config['gpt_res'].get('gpt_model', None)
    gpt_prompt = config['gpt_res'].get('gpt_prompt', None)
    gpt_file_path = config['gpt_res'].get('gpt_file_path', None)
    gpt_api_key = config['gpt_res']['gpt_api_key']

    todays_date = "{:%Y_%m_%d}".format(datetime.now())


    model = t.TFSegformerForSemanticSegmentation.from_pretrained(model_path)  

    session = boto3.Session()
    client = session.client(profile)

    color_dict = load_color_values(val_color_csv_path)
    # groundtruth_df = pd.read_csv(gt_csv_path)
    input_df = pd.read_csv(input_csv_path)
    input_df['ground_truth_g']=input_df['ground_truth_kg']*1000
    input_df['mask'] = ''
    input_df['final_image'] = ''
    input_df['pixel_count'] = 0
    input_df['histogram'] = ''
    input_df['pred_w2'] = 0.0
    input_df['error'] = 0.0
    input_df['success'] = False
    model_final_name = model_name + model_version
    input_df['model_version']= model_final_name
    if gpt_response:
        input_df['gpt_result'] = 0.0
        input_df['gpt_error'] = 0.0
        input_df['gpt_success'] = False

    #use_input_groundtruth = 'input_groundtruth' in input_df.columns

    entries = []
    for _, row in input_df.iterrows():
        image_dict = split_filename(row['s3_image_path'])
        local_image_folder = path_to_save_images + image_dict['site_id'] + '/' + image_dict['food_item'] + '/'
        os.makedirs(local_image_folder, exist_ok=True)
        local_image_path = path_to_save_images + image_dict['site_id'] + '/' + image_dict['food_item'] + '/' + image_dict['image'] + '.jpeg'
        if os.path.exists(local_image_path) and replace_images is False:
            if logger:
                logger.info(f"Image {local_image_path} already exists. Skipping download.")   
        else:
            img_temp = download_image(bucket, row['s3_image_path'], client)
            img_temp.save(local_image_path)
        site_id = image_dict['site_id']
        #taxonomy_code = row['taxonomy_code']
        food_item = image_dict['food_item']
        #input_groundtruth = row['input_groundtruth'] if use_input_groundtruth else 0

        s3_reference_image_path = row['s3_reference_image_path']
        if s3_reference_image_path is None:
            if logger:
                logger.error(f"No reference image found for image {local_image_path}. Skipping image.")
            continue
        else:
            s3_reference_weight = row['ground_truth_g']
            rework_g = row['rework_kg']*1000
            if local_image_path and site_id and food_item:
                #composed_key = f"{site_id}_{taxonomy_code}"
                entries.append((site_id, local_image_path, food_item,local_image_folder,image_dict['image'],
                                s3_reference_image_path,s3_reference_weight,rework_g,model_final_name))
    
    if not entries:
        if logger:
            logger.error("No valid entries found in the CSV file")
        raise ValueError("No valid entries found in the CSV file")
    
    #results = []
    for index, (site_id, local_image_path, food_item,local_image_folder,image_dict_name,reference_image,reference_image_gt,rework_g,model_final_name) in enumerate(entries):
        try:
            key = f"{food_item}_{model_final_name}"
            if key not in color_dict:
                if logger:
                    logger.error(f"No color found for key {food_item}. Skipping image {local_image_path}.")
                input_df.at[index, 'success'] = False
                continue
            colors = color_dict[key]
        
            if food_item in equalizer_items:
                equalizer = True
            else:
                equalizer = False
            masked_img = get_seg(local_image_path, model, mask_val=mask_model_val, resize=True, new_bg_removal=new_bg_removal, equalize=equalizer)

            final_mask = get_final_mask_filter( masked_img, colors=colors, val=final_mask_vals, logger=logger)

            # if save_plots:
            #     mask_image = Image.fromarray(final_mask.astype(np.uint8))
            #     mask_image_path = local_image_folder + f"{food_item}_mask_{final_mask_vals}.png"
            #     mask_image.save(mask_image_path)
            #     input_df.at[index, 'mask'] = mask_image_path
            # else:
            #     input_df.at[index, 'mask'] = ''

            new_final_img = get_final_img(local_image_path, final_mask,mask_val)  ## saving final mask with the image
            if save_plots:
                final_image_path = local_image_folder + image_dict_name + "_" +todays_date  +"_final_mask.png"
                temp_img= Image.fromarray(new_final_img)
                temp_img.save(final_image_path)
                input_df.at[index, 'mask'] = final_image_path
            else:
                input_df.at[index, 'mask'] = ''

            new_histogram, _ = get_histogram(new_final_img)

            pixel_count = new_histogram[-1]
            pixel_count = pixel_count.astype(int)
            input_df.at[index, 'pixel_count'] = pixel_count

            if save_plots:
                plt.figure()
                plt.plot(new_histogram)
                plt.savefig(local_image_folder + f"{image_dict_name}_{todays_date}_histogram.png")
                plt.close()

            #reference_row = groundtruth_df[groundtruth_df['taxonomy_code'] == taxonomy_code]
            # if not reference_row.empty:
            #     reference_pixel_count = reference_row.iloc[0]['reference_pixel_count']
            #     groundtruth_weight = reference_row.iloc[0]['groundtruth']

            #     weight2 = input_groundtruth if input_groundtruth else 0
            #     pred_w2, error = get_val(reference_pixel_count, pixel_count, groundtruth_weight, weight2)
            # else:
            #     if logger:
            #         logger.error(f"No groundtruth data found for taxonomy_code {taxonomy_code}.")
        
            #reference_pixel_count, reference_image_weight =get_reference_data(reference_image,model_version,reference_file)
            
            ## get refrence image pixel data
            if os.path.exists(reference_image) is False:
                ref_image = download_image(bucket, reference_image, client)
                ref_dict = split_filename(reference_image)
                ref_image_path = path_to_save_images + ref_dict['site_id'] + '/' + ref_dict['food_item'] + '/' + ref_dict['image'] + '.jpeg'
                ref_image.save(ref_image_path)
            masked_img_ref = get_seg(ref_image_path, model, mask_val=mask_model_val, resize=True, new_bg_removal=new_bg_removal, equalize=equalizer)
            final_mask_ref = get_final_mask_filter(masked_img_ref, colors=colors, val=final_mask_vals,show=False, logger=logger)
            new_final_img_ref = get_final_img(ref_image_path, final_mask_ref,mask_val)  ## saving final mask with the image
            if save_plots:
                final_image_path_ref = local_image_folder + ref_dict['image'] +"_final_mask.png"
                if os.path.exists(final_image_path_ref):
                    os.remove(final_image_path_ref)
                temp_img= Image.fromarray(new_final_img_ref)
                temp_img.save(final_image_path_ref)
            new_histogram_ref, _ = get_histogram(new_final_img_ref)
            pixel_count_ref = new_histogram_ref[-1]
            pixel_count_ref = pixel_count_ref.astype(int)

            pred_w2, error = get_val(pixel_count_ref, pixel_count, reference_image_gt, rework_g)

            input_df.at[index, 'pred_w2'] = pred_w2
            input_df.at[index, 'error'] = error

            if gpt_response:
                gpt_result = get_count(image_path = local_image_path, item = food_item, api_key = gpt_api_key, df_loc = gpt_file_path, prompt = gpt_prompt)
                gpt_error = (rework_g-gpt_result)/rework_g if rework_g !=0 else 0
                input_df.at[index, 'gpt_result'] = gpt_result
                input_df.at[index, 'gpt_error'] = gpt_error
                input_df.at[index, 'gpt_success'] = True if gpt_result is not None else False
            
            input_df.at[index, 'success'] = True if pred_w2 > 0.00 else False

            #results.append((masked_img, final_mask, new_final_img, new_histogram, pred_w2, error, gpt_result, gpt_error))
        except Exception as e:
            if logger:
                logger.error(f"Error processing image {local_image_path}: {e}")
            input_df.at[index, 'success'] = False
            continue
    
    output_csv_dir = path_to_save_images + 'output_csv/'
    os.makedirs(output_csv_dir, exist_ok=True)
    output_csv_path = os.path.join(output_csv_dir, f"output_{todays_date}.csv")
    input_df.to_csv(output_csv_path, index=False)

    if logger:
        logger.info(f"Processing complete. Output saved to {output_csv_path}")

    try:
        temp_pd = input_df[['site_id','food_item_label','ground_truth_g','pred_w2','error','success']]
        if gpt_response:
            temp_pd['gpt_result'] = input_df['gpt_result']
            temp_pd['gpt_error'] = input_df['gpt_error']
    except Exception as e:
        if logger:
            logger.error(f"Error sending message to slack: {e}")
    
    if slack_post:
        send_message_to_slack(temp_pd, is_df=True,url=slack_webhook,tabulate_type='fancy_grid')

    return input_df 
    #return output_csv_path, results