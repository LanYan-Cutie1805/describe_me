from together import Together
import base64
import os
import tkinter as tk 
from tkinter import filedialog

client = Together(api_key = "8fc24c8984e433c5ed5764cf3ecd7d6bf428524042f2f01708b935572ae19db5")

# Open the file to get picture
def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    
    if not file_path:
        print("No file selected.")
        exit(1)
    return file_path

# imagePath= "hoyofest.jpg"
getDescriptionPrompt = "describe the image"

image_path = select_image()

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: {image_path} not found.")
        exit(1)


base64_image = encode_image(image_path)

stream = client.chat.completions.create(
    model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": getDescriptionPrompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "" if chunk.choices else "", end="", flush=True)