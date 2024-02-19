import numpy as np
import pytest

from app.encoding import encode_image, decode_image


@pytest.fixture()
def image() -> np.ndarray:
    return np.array(
        [[163, 162, 190, 192, 170, 191, 172, 172, 178, 183], [162, 188, 185, 196, 202, 200, 198, 186, 179, 156],
         [196, 193, 194, 202, 193, 212, 203, 194, 184, 171], [206, 204, 201, 200, 198, 173, 186, 189, 185, 186],
         [201, 204, 199, 202, 172, 162, 174, 198, 200, 185], [202, 197, 200, 205, 166, 167, 169, 185, 197, 194],
         [163, 165, 166, 159, 145, 148, 154, 154, 172, 161], [118, 128, 120, 108, 112, 117, 113, 118, 139, 132],
         [96, 93, 89, 82, 87, 79, 83, 95, 76, 93], [66, 72, 64, 73, 68, 59, 71, 71, 69, 69]],
        ">u2")


@pytest.fixture()
def encoded_image_ref() -> str:
    return "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKEAAAAAD4yUwiAAAAjUlEQVR4nCXJQUrDQBQA0DeT+cEp0aDQTXEhHsWreiRB6AF0UXBhbWlimsSFb/uSV6tH2cHWF1qRrXYmxZNq507ykT0LVeuiE26EvthYzBZh71Yj6bMJi+zT2UnVW7NklDR+hcmPWS32/uOo0fr24Fy82RicFOEqbI3FwexqFAZF59198qI1qCYXHRb+AAqCKwySwEUfAAAAAElFTkSuQmCC"


def test_encode_image(image, encoded_image_ref):
    encoded_image = encode_image(image)
    assert len(encoded_image) == len(encoded_image_ref), "Unexpected result for encoded image"
    assert encoded_image == encoded_image_ref, "Unexpected result for encoded image"


def test_decode_image(image, encoded_image_ref):
    decoded_image = decode_image(encoded_image_ref)
    assert np.shape(image) == np.shape(decoded_image), "Unexpected dimensions for decoded image"
    assert np.array_equal(decoded_image, image), "Unexpected result for decoded image"
