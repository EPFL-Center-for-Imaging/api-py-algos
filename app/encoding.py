import base64
import io

import numpy as np
from PIL import Image


def decode_image(b64data: str) -> np.ndarray:
    """
    Decode a Base64 encoded string into a np.ndarray
    From ksugar's samapi https://github.com/ksugar/samapi/blob/3c93d64497051ebb34ddeacd47153313bf31a5b5/src/samapi/utils.py#L12
    """
    return np.array(Image.open(io.BytesIO(base64.b64decode(b64data))))


def encode_image(data: np.ndarray) -> str:
    """
    Encode a np.ndarray into a Base64 encoded string
    """
    img = Image.fromarray(data)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, "PNG")
    return base64.b64encode(img_byte_arr.getvalue()).decode()
