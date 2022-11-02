import requests
import numpy as np
import cv2
import json
import base64
from PIL import Image
from io import BytesIO
#from bs4 import BeautifulSoup

MIXED_REALITY_DEVICE_PORTAL_USERNAME = "acelab"
MIXED_REALITY_DEVICE_PORTAL_PASSWORD = "ace1ace!"
HOLOLENS_IP_ADDR = "http://"+MIXED_REALITY_DEVICE_PORTAL_USERNAME + \
    ":"+MIXED_REALITY_DEVICE_PORTAL_PASSWORD+"@"+"192.168.0.114"


def getPhoto():
    response = requests.post(url=HOLOLENS_IP_ADDR +
                             '/api/holographic/mrc/photo?holo=false&pv=true')
    encoded_file_name = str(base64.b64encode(
        (json.loads(response.text)["PhotoFileName"]).encode('ascii')).decode('ascii'))
    # print(encoded_file_name)
    response_image = requests.get(
        url=HOLOLENS_IP_ADDR + '/api/holographic/mrc/file?filename=' + encoded_file_name)
    base64_encoded_image = base64.b64encode(response_image.content)
    #open("instagram.png", "wb").write(response_image.content)
    # return response
    #im = Image.open(BytesIO(base64.b64decode(response_image)))
    # print(response_image)
    # im.show()
    return base64_encoded_image
