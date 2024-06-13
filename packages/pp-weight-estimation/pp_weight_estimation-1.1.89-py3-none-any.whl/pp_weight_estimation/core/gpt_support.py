# We will use the OpenAI API to get the result of the image

import base64
import requests


prompt = "Count the number of {item} in the image and just return the number"
prompt2 = "Based on the reference image of weight {item}, what is the weight of the 2nd image? Please respond only in the format '{item}: amount'."


# OpenAI API Key
api_key = None

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_gpt_result(image_path ,ref_image_path,ref_image_weight, api_key,prompt=prompt):
    # Getting the base64 string
    base64_image = encode_image(image_path)
    ref_base64_image = encode_image(ref_image_path)

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
            "text": prompt.format(item=ref_image_weight)
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{ref_base64_image}"
            }
            },
            {            
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            },
        ]
        }
    ],
    "max_tokens": 300}

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
    return response