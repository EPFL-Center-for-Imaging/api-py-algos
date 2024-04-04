import time

import numpy as np

from .compute_features import get_features_from_segm_mask


def draw_mask(image: np.ndarray) -> np.ndarray:
    mask = np.zeros(shape=(image.shape[0], image.shape[1]), dtype=">u2")
    hw_ratio = 12
    n, m = mask.shape[0], mask.shape[1]
    mask[n // 4 - n // hw_ratio: n // 4 + n // hw_ratio, m // 4 - m // hw_ratio: m // 4 + m // hw_ratio] = 1
    mask[n // 4 - n // hw_ratio: n // 4 + n // hw_ratio, 3 * m // 4 - m // hw_ratio: 3 * m // 4 + m // hw_ratio] = 2
    for i in range(0, n // 4):
        dj = int(np.round(m // 4 - i * (m // 4 - m // 8) / (n // 4)))
        mask[n // 2 + i, m // 2 - dj: m // 2 + dj] = 3
    return mask


def run_example(data: np.ndarray, **kwargs) -> {}:
    # The algorithm parameters
    print("Parameters: ", kwargs)

    # Details of failed assertions or raised exceptions will be passed on to the server via an HTTP exception
    assert data.ndim >= 2, "Expecting 2D image (single channel or RGB)"

    # Process the data
    # time.sleep(5)
    mask = draw_mask(data)

    if data.ndim == 2:
        result_image = np.where(mask > 0, data, mask)
    else:
        result_image = np.zeros_like(data)
        for i in np.arange(data.shape[2]):
            result_image[:, :, i] = np.where(mask > 0, data[:, :, i], mask)

    # Compute the geojson.Feature for each object from the mask
    features = get_features_from_segm_mask(mask)

    # Add measurements and classification to each feature by updating its properties
    # For QuPath: the measurements value should be a number (not a string)
    #             the classification value can be "Positive"/"Negative"/"1+"/"2+"/"3+" or anything else (as string)
    metrics = [10, 20.42, 30.5]
    classifications = ["Positive", "Positive", "Negative"]
    features[0].properties.update({"Classification": classifications[0]})
    for feature, metric, classification in zip(features, metrics, classifications):
        feature.properties.update({
            "Metric from Python": float(metric),
            "Classification": classification
        })

    # The keys in the output dictionary should match the "output_endpoints" values in the algo definition
    return {"image": result_image, "features": features}
