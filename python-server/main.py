from tkinter import Image
from fastapi import FastAPI, UploadFile, WebSocket
import crop
import sketch_recognition
import hololens2_utilities

app = FastAPI()


@app.post("/slbb")
def root():
    # return get3DModelFromLocalDatabase(preditObjectFromSketch(cropPageFromImage(img)))

    return get3DModelFromLocalDatabase(preditObjectFromSketch(cropPageFromImage(hololens2_utilities.getPhoto())))


def get3DModelFromLocalDatabase(object_name):
    return {"Items": from_local_hololens_database(object_name)}


def from_local_hololens_database(object_name):
    data = []
    data.append({"model_url": object_name})
    return data


def preditObjectFromSketch(image):
    return sketch_recognition.sketch_predicted_object(image)


def cropPageFromImage(image):
    return crop.getSketchFromPage(image)
