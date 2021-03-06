import base64
import io
from typing import List

from fastapi import FastAPI
import numpy as np
from PIL import Image
from pydantic import BaseModel

from corebreakout import CoreSegmenter
from coreapi.config import CONFIG

# By default, models from corebreakout's assets.zip
def load_model():
    return CoreSegmenter(**CONFIG)

app = FastAPI()


# Define classes for what Label-tool accepts

class InputBytes(BaseModel):
    b64: str


class Instance(BaseModel):
    input_bytes: InputBytes


class Instances(BaseModel):
    instances: List[Instance]


@app.post("/labels")
async def core_labels(images: Instances):
    labels = []
    for instance in images:
        labels.append(segment_image(instance))


def segment_image(instance: Instance, model=load_model()):
    image_bytes = base64.decodebytes(instance[1][0].input_bytes.b64.encode())
    image_arr = np.array(Image.open(io.BytesIO(image_bytes)))
    return model.segment(image_arr)
