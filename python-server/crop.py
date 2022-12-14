#!/usr/bin/env python3

import cv2
import numpy as np
import glob
import os
from pathlib import Path
from pprint import pprint as pp
import base64
from PIL import Image

path_in = 'in/*'
path_out = 'out'
window_name = 'crop'
size_max_image = 1000
debug_mode = False


def create_opencv_image_from_base64(base64_encoded_image):
    im_bytes = base64.b64decode(base64_encoded_image)
    img_array = np.frombuffer(im_bytes, dtype=np.uint8)
    return cv2.imdecode(img_array, 1)


def get_image_width_height(image):
    image_width = image.shape[1]  # current image's width
    image_height = image.shape[0]  # current image's height
    return image_width, image_height


def calculate_scaled_dimension(scale, image):
    # http://www.pyimagesearch.com/2014/01/20/basic-image-manipulations-in-python-and-opencv-resizing-scaling-rotating-and-cropping/
    image_width, image_height = get_image_width_height(image)
    ratio_of_new_with_to_old = scale / image_width
    dimension = (scale, int(image_height * ratio_of_new_with_to_old))
    return dimension


def rotate_image(image, degree=90):
    # http://www.pyimagesearch.com/2014/01/20/basic-image-manipulations-in-python-and-opencv-resizing-scaling-rotating-and-cropping/
    image_width, image_height = get_image_width_height(image)
    center = (image_width / 2, image_height / 2)
    M = cv2.getRotationMatrix2D(center, degree, 1.0)
    image_rotated = cv2.warpAffine(image, M, (image_width, image_height))
    return image_rotated


def scale_image(image, size):
    image_resized_scaled = cv2.resize(
        image,
        calculate_scaled_dimension(
            size,
            image
        ),
        interpolation=cv2.INTER_AREA
    )
    return image_resized_scaled


def detect_box(image, cropIt=True):
    # https://stackoverflow.com/questions/36982736/how-to-crop-biggest-rectangle-out-of-an-image/36988763
    # Transform colorspace to YUV
    image_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image_y = np.zeros(image_yuv.shape[0:2], np.uint8)
    image_y[:, :] = image_yuv[:, :, 0]

    # Blur to filter high frequency noises
    image_blurred = cv2.GaussianBlur(image_y, (3, 3), 0)
    if (debug_mode):
        show_image(image_blurred, window_name)

    # Apply canny edge-detector
    edges = cv2.Canny(image_blurred, 100, 400, apertureSize=3)
    if (debug_mode):
        show_image(edges, window_name)

    # Find extrem outer contours
    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if (debug_mode):
        #                                      b  g   r
        cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
        show_image(image, window_name)

    # https://stackoverflow.com/questions/37803903/opencv-and-python-for-auto-cropping
    # Remove large countours
    new_contours = []
    for c in contours:
        if cv2.contourArea(c) < 4000000:
            new_contours.append(c)

    # Get overall bounding box
    best_box = [-1, -1, -1, -1]
    for c in new_contours:
        x, y, w, h = cv2.boundingRect(c)
        if best_box[0] < 0:
            best_box = [x, y, x + w, y + h]
        else:
            if x < best_box[0]:
                best_box[0] = x
            if y < best_box[1]:
                best_box[1] = y
            if x + w > best_box[2]:
                best_box[2] = x + w
            if y + h > best_box[3]:
                best_box[3] = y + h

    if (debug_mode):
        cv2.rectangle(image, (best_box[0], best_box[1]),
                      (best_box[2], best_box[3]), (0, 255, 0), 1)
        show_image(image, window_name)

    if (cropIt):
        image = image[best_box[1]:best_box[3], best_box[0]:best_box[2]]
        if (debug_mode):
            show_image(image, window_name)

    return image


def show_image(image, window_name):
    # Show image
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, image)
    image_width, image_height = get_image_width_height(image)
    cv2.resizeWindow(window_name, image_width, image_height)

    # Wait before closing
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def cut_of_top(image, pixel):
    image_width, image_height = get_image_width_height(image)

    # startY, endY, startX, endX coordinates
    new_y = 0+pixel
    image = image[new_y:image_height, 0:image_width]
    return image


def cut_of_bottom(image, pixel):
    image_width, image_height = get_image_width_height(image)

    # startY, endY, startX, endX coordinates
    new_height = image_height-pixel
    image = image[0:new_height, 0:image_width]
    return image


def convert_bw(img):
    # convert to Black and White image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshed = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return threshed


def getSketchFromPage(base64_encoded_image):
    # fastapi sample test
    #image = Image.open(base64_encoded_image.file)
    #image = np.array(image)

    # base64 image
    image = create_opencv_image_from_base64(base64_encoded_image)

    #image = rotate_image(image)
    image = cut_of_bottom(image, 1000)

    image = scale_image(image, size_max_image)
    if (debug_mode):
        show_image(image, window_name)

    image = detect_box(image, True)

    image = convert_bw(image)
    # Create out path
    if not os.path.exists(path_out):
        os.makedirs(path_out)

    center = image.shape
    w = center[1]/50
    h = center[0]/50
    x = center[1]/2
    y = center[0]/2

    #image = image[int(h):int(2*y-h), int(w):int(2*x+w)]
    # Build output file path
    #file_name_ext = os.path.basename(file_iterator)
    #file_name, file_extension = os.path.splitext(file_name_ext)
    #file_path = os.path.join(path_out, file_name + '.cropped' + file_extension)

    image = cv2.bitwise_not(image)

    retval, buffer = cv2.imencode('.jpg', image)
    cv2.imwrite("./out/result.jpg", image)
    return buffer
