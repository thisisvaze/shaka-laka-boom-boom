import base64
import requests
from PIL import Image
import gradio as gr
import json


def sketch_predicted_object(image):
    images = base64.b64encode(image).decode('utf-8')
    # print(images)
    response = requests.post(url='https://hf.space/embed/thisisvaze/line-drawing-object-prediction/+/api/predict',
                             json={"data": ["data:image/png;base64," + str(images)]}).json()
    print(response)
    # return "none"
    # return response
    if (response["data"][0]["confidences"][0]["confidence"] > 0.15):
        return response["data"][0]["label"]
    else:
        return "none"
