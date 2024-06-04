import base64
import io

import numpy as np
from PIL import Image

# Remove the limit of the image size (for trusted data)
Image.MAX_IMAGE_PIXELS = None


def decode_image_bytes(data: bytes) -> np.ndarray or None:
    """
    Decode an encoded image as bytes into a np.ndarray
    """
    return np.array(Image.open(io.BytesIO(data)))


def decode_image(b64data: str) -> np.ndarray or None:
    """
    Decode a Base64 encoded string into a np.ndarray
    From ksugar's samapi https://github.com/ksugar/samapi/blob/3c93d64497051ebb34ddeacd47153313bf31a5b5/src/samapi/utils.py#L12
    """
    if b64data is None:
        return None
    return decode_image_bytes(base64.b64decode(b64data))


def encode_image(data: np.ndarray) -> str:
    """
    Encode a np.ndarray into a Base64 encoded string
    """
    if data is None:
        return ''
    img = Image.fromarray(data)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, "TIFF")
    return base64.b64encode(img_byte_arr.getvalue()).decode()
