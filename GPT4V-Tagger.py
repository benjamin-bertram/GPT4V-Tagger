import os
import base64
import requests
import json

# Set your OpenAI API key here
api_key = "OPENAI KEY"

# Function to encode the image in base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to process the image and get tags
def get_image_tags(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {   
                "role": "system", 
                "content": "You are a helpful assistant and tag the image as detailed as possible by filling the variables accordingly: A bagpipe [Action Description] by [ethnic Subject Description], [haircolor and hairstyle], [cloth item1], [cloth item2], [cloth item3], [cloth item4], [Depth of field], [Quality Mediatype], [Perspective/Camera Angle], [Camera framing], [lighting], [Notable accesories], [Background/Location]"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    # Print the response for debugging
    print(json.dumps(response.json(), indent=4))
    return response.json()

# Directory containing images
image_directory = 'Captions'

# Loop through all JPEG images in the folder
for filename in os.listdir(image_directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(image_directory, filename)
        base64_image = encode_image(image_path)
        response = get_image_tags(base64_image)

        # Save the response in a .txt file
        txt_filename = os.path.splitext(filename)[0] + '.txt'
        with open(os.path.join(image_directory, txt_filename), 'w') as file:
            if response.get("choices"):
                content = response["choices"][0]["message"]["content"]
                file.write(content)       
                print(filename," tagged")         
            else:
                file.write("No content found.")

print("Image tagging completed.")
