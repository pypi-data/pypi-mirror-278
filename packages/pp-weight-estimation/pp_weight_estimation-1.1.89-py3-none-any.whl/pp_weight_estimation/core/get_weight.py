### File for getting weight estimates from images

import transformers as t
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from rembg import remove ## for background removal -needed for some sites 
from PIL import Image
import skimage
from skimage.util import img_as_ubyte

__all__ = ["get_segformer", "get_biggest_contours", "get_seg", "get_final_mask", "get_final_img", "get_final_mask_filter",
           "get_histogram", "get_weight", "get_val", "split_filename"]

model_checkpoint = '/home/malav/wml_packges/mit-segformer-s' # download one of the pretrained models from S3 to your local device

def get_segformer(model_checkpoint=None) :
    """
    Function to get the Segformer model
    """
    return t.TFSegformerForSemanticSegmentation.from_pretrained(model_checkpoint)


def get_biggest_contours(contours):
    """
    Returns the biggest contour from a list of contours
    """
    val = 0
    final_contour = [contours[0]]
    for counter in contours:
        x,y,width,height = cv2.boundingRect(counter)
        #w_val = width-x
        #h_val = height-y
        #area = w_val*h_val
        area = width*height
        if area>val:
            val = area
            final_contour=[x,y,width,height]
    return final_contour


def get_seg(img,model,mask_val=0.08,resize=True,new_bg_removal=False,equalize=False,show=False,logger=None):
    """
    Function to get the segmentation mask
    """
    if isinstance(img,str):
        if new_bg_removal:
            image = Image.fromarray(np.array(remove(Image.open(img))))
        else:
            image = Image.open(img)
        if show:
            plt.imshow(image)
    else:
        if new_bg_removal:
            image = Image.fromarray(np.array(remove(img)))
        else:
            image = Image.open(img) 
        if show:
            plt.imshow(image)   
    if equalize:
        image = Image.fromarray(img_as_ubyte(skimage.exposure.equalize_adapthist(np.array(image), clip_limit=0.03)))
        if show:
            plt.imshow(image)
    if resize:
        image = image.resize((1600,1200))
    image_ori = image.copy()
    image_np = np.array(image_ori)
    
    mean = tf.constant([0.485, 0.456, 0.406])
    std = tf.constant([0.229, 0.224, 0.225])
    
    image = tf.convert_to_tensor(image_np)[:, :, :3]
    before_im = tf.convert_to_tensor(np.zeros(image.shape, dtype=np.float32))
    after_im = (tf.cast(image, tf.float32)/255. - mean) / std
    tensor = tf.concat([before_im,  after_im], axis=-1)
    tensor = tf.image.resize(tf.expand_dims(tensor, axis=0), [512, 512])
    tensor = tf.transpose(tensor, (0, 3, 1, 2))
    mask = model(tensor).logits[0, 1]
    mask = tf.image.resize(tf.expand_dims(tf.math.sigmoid(mask), -1), image.shape[:2]).numpy()
    mask_old = mask.copy()
    
    mask = np.where(mask>mask_val,mask,0)
    mask = np.where(mask<mask_val,mask,1)
    
    mask = np.array(mask, np.uint8)
    mask_res_np = np.array(mask)
    
    # contours, _ = cv2.findContours(mask_res_np[:,:], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    # for contour in contours:
    #     x, y, width, height = cv2.boundingRect(contour)
    #     print("Bounding Box Coordinates: ", x, y, x + width, y + height)
    # biggest_contours = get_biggest_contours(contours)
    # if logger:
    #     logger.info(biggest_contours)
    mask = cv2.normalize(mask_res_np, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    
    mask_box = np.zeros(mask_res_np.shape, dtype=np.uint8)
    #cv2.rectangle(mask_box, (biggest_contours[0], biggest_contours[1],biggest_contours[2], biggest_contours[3]), 255, -1)    
    mask_res_np[mask_box <= 0.5] = 0
    #plt.imshow(mask_box)

    masked_image = np.copy(image_np)
    masked_image[mask<= 0.5] = 0
    #plt.imshow(masked_image)
    
    if equalize==False:
        masked_image = masked_image[:,:,:3]
        
    if show:
        f1, axarr1 = plt.subplots(1,2,figsize=(15,15),gridspec_kw={'wspace':0.1, 'hspace':0.1},squeeze=True)        
        axarr1[0].imshow(mask_box,cmap='gray')
        axarr1[1].imshow(masked_image)
       
    # color = (0, 255, 0) 
    # thickness = 2
    # cv2.rectangle(image_np, (biggest_contours[0], biggest_contours[1], biggest_contours[2], biggest_contours[3]), color, thickness)

    if show:
        f, axarr = plt.subplots(2,2,figsize=(15,15),gridspec_kw={'wspace':0.1, 'hspace':0.1},squeeze=True)
        axarr[0,0].imshow(image)
        axarr[0,1].imshow(mask_old)
        axarr[1,0].imshow(mask)
        axarr[1,1].imshow(image_np)   
    
    return masked_image

def get_final_mask(masked_img,color,val =55,logger=None):
    """
    Function to get the final mask
    """
    upper_bound = [i+val for i in color]
    lower_bound = [i-val for i in color]
    # if logger:
    #     logger.info(upper_bound)
    #     logger.info(lower_bound)
    final_img = cv2.inRange(masked_img, np.array(lower_bound), np.array(upper_bound))

    # new_masked_image = masked_img.copy()
    # new_masked_image[final_img<= 0.5] = 0
    # if show:
    #     f, (axarr,axarr2) = plt.subplots(1,2,figsize=(15,15),gridspec_kw={'wspace':0.1, 'hspace':0.1},squeeze=True)
    #     axarr.imshow(final_img)
    #     axarr2.imshow(new_masked_image)
    return final_img

def get_final_mask_filter(masked_image,colors=None,val=55,show=False,logger=None):   
    # new_image = masked_image.copy()

    if colors is None:
        return masked_image
    
    # for color in colors:
    #     new_image = get_final_mask(new_image,color,val,show=show,logger=logger)
    # new_image[(new_image < 15).all(axis=2)] = [0, 0, 0]
    # return new_image
    combined_mask = np.zeros(masked_image.shape[:2], dtype=np.uint8)

    for color in colors:
        final_mask = get_final_mask(masked_image, color, val, logger=logger)
        combined_mask = cv2.bitwise_or(combined_mask, final_mask)
    
    # Apply the combined mask to the original image
    new_masked_image = masked_image.copy()
    new_masked_image[combined_mask <= 0.5] = 0
    
    if show:
        f, (axarr, axarr2) = plt.subplots(1, 2, figsize=(15, 15), gridspec_kw={'wspace': 0.1, 'hspace': 0.1}, squeeze=True)
        axarr.imshow(combined_mask, cmap='gray')
        axarr2.imshow(new_masked_image)
    
    return new_masked_image


def get_final_img(img,mask,mask_val=0.3):
    """
    Function to get the final image
    """
    new_masked_image = np.copy(Image.open(img))
    if new_masked_image.shape[0]==1600:
        new_masked_image = cv2.resize(new_masked_image, (1600, 1200), interpolation = cv2.INTER_AREA)
    new_masked_image[mask<= mask_val] = 0
    return new_masked_image
    
def get_histogram(img,show=False,logger=None):
    """
    Function to get the histogram of the image
    """
    img = np.where(img<10,img, 100)
    histogram, bin_edges, patches = plt.hist(img.ravel())
    if logger:
        logger.info('histogram :  {}'.format(histogram))
        logger.info('bin edges : {}'.format(bin_edges))
    if show:
        plt.figure()
        plt.plot(bin_edges[:-1], histogram)
        plt.show()
    return histogram, bin_edges

def get_weight(img,model,**kwargs):
    """
    Function to get the weight of the object in the image
    """
    mask = get_seg(img,model,**kwargs)
    get_histogram(mask,)
    return np.sum(mask)

def get_val(pix1,pix2,weight1,weight2,logger=None):
    """
    Function to get the histogram error
    """
    pred_w2 = weight1*(pix2/pix1)
    if weight2 == 0:
        error = 0.0
    else:
        error = ((abs(weight2-pred_w2))/weight2)*100 if weight2 !=0 else 0.0
    if logger:
        logger.info(pred_w2)
        logger.info(error)
    return pred_w2,error

# def get_reference_data(file_name,model,data_file_path,logger=None):
#     """
#     Function to get the reference data of each reference image with model version
#     """

#     pass

def split_filename(file: str,logger=None) -> dict :
    """
    Function to split the filename into parts
    """
    parts = file.split('/')
    if logger:
        logger.info(parts)
    return {
        'site_id': parts[0][7:],
        'meal_service': parts[1][12:],
        'food_item': parts[2][9:],
        'image': parts[3][6:-13]
    }