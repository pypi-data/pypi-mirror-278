## function to send csv file to slack channel

from slack_sdk import WebhookClient, WebClient
import os
import pandas as pd
import tabulate

__all__ = ['send_file_to_slack','send_message_to_slack','get_slack_webhook']

def send_file_to_slack(file_path,slack_token,slack_channel):
    """
    Function to send the file to slack channel
    """
    try :
        
        client = WebClient(token=slack_token)
        response = client.files_upload(
            channels=slack_channel,
            file=file_path)
        return response
    except Exception as e:
        return e
    
# slack_webhook = 'https://hooks.slack.com/services/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' ## pp_image_weight_estimation

def get_slack_webhook(slack_channel='pp_image_weight_estimation'):
    """
    Function to get the slack webhook
    """
    if slack_channel=='pp_image_weight_estimation':
        slack_webhook = "https://hooks.slack.com/services/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"
        #slack_webhook = 'https://hooks.slack.com/services/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'
        #slack_webhook = 'https://hooks.slack.com/services/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'
        #slack_webhook = 'https://hooks.slack.com/services/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'
    else:
        return 'Invalid slack channel'
    return slack_webhook

## new slack_webhook ='https://hooks.slack.com/services/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'

def send_message_to_slack(message,slack_channel='pp_image_weight_estimation',is_df=False,tabulate_type='fancy_grid',url=None,**kwargs):
    """
    Function to send the message to slack channel. Msg should be a json file. (CSV file not good for this function)
    Args:
        message : str : message to be sent or pd.DataFrame : dataframe to be sent
        is_df : bool : whether the message is a dataframe or not. If True, the message will be taken as a string to be loaded in a dataframe
        slack_webhook : str : webhook url for the slack channel
        tabulate_type : str : type of tabulation to be done. Default is 'orgtbl'. Other is 'grid'
    """
    try :
        slack_webhook = get_slack_webhook(slack_channel)
        if slack_webhook is 'Invalid slack channel':
            slack_webhook = url
        if url:
            slack_webhook = url
        client = WebhookClient(url=slack_webhook)
        if is_df:
            #df = pd.read_csv(message)
            tab = (tabulate.tabulate(message,headers=list(message.columns), tablefmt=tabulate_type,floatfmt='.3f',**kwargs))
            slack_table = {"text":"```\n" + tab + "\n```"}
            info = slack_table['text']
            response = client.send(text=info)
        else:

            response = client.send(text=message)
        return response
    except Exception as e:
        return e