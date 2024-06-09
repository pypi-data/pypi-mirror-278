import base64
from io import BytesIO

from PIL import Image


def load_image_base64(image_base64: str):
    _, image_base64 = image_base64.split(",", 1)
    bytes = base64.b64decode(image_base64)
    return Image.open(BytesIO(bytes))
