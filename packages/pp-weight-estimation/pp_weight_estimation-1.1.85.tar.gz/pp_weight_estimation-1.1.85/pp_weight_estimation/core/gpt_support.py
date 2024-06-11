## adding chatgpt support for counting items in image

import pandas as pd
import os
import base64
import requests

# loading the reference item weight from the reference file
def load_ref_weight(ref_file):
    """
    Function to load the reference weight
    """
    ref_df = pd.read_csv(ref_file)
    return ref_df

prompt = "Count the number of {item} in the image and just return the number"

# OpenAI API Key
api_key = "YOUR_OPENAI_API_KEY"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def get_count(image_path ,item, api_key,df_loc='../ref_file.csv',prompt=prompt):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    t1 = load_ref_weight(df_loc)
    t1_weight = t1[t1['item'] == item]['item_individual_weight'].values[0]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}

    payload = {
    "model": "gpt-4o",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt.format(item=item)
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300}

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
    print(t1_weight)