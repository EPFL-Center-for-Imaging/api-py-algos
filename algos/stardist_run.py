import numpy as np
from csbdeep.utils import normalize
from stardist.models import StarDist2D

from .compute_features import get_features_from_segm_mask


def run_stardist(data: np.ndarray, **kwargs) -> {}:
    if not isinstance(data, np.ndarray):
        raise TypeError(type(data))

    # Get the model based on the data dimensions (2D single channel or 2D RGB)
    if data.ndim == 2:
        # "2D_versatile_fluo", "2D_paper_DSB2018": Fluorescence (nuclear marker) -> 2D single channel
        model_name = "2D_versatile_fluo"
    elif data.ndim == 3 and data.shape[2] == 3:
        # "2D_versatile_he": Brightfield (H&E) -> 2D RGB
        model_name = "2D_versatile_he"
    else:
        raise ValueError(f"Unexpected data ndim = {data.ndim}")

    model = StarDist2D.from_pretrained(model_name)

    block_size = kwargs.get("block_size")
    if (data.shape[0] > block_size) or (data.shape[1] > block_size):
        labels, polys = model.predict_instances_big(normalize(data), axes="YXC", **kwargs)
    else:
        kwargs.pop("block_size")
        kwargs.pop("min_overlap")
        labels, polys = model.predict_instances(normalize(data), **kwargs)

    # Compute the geojson.Feature for each object from the segmentation mask
    features = get_features_from_segm_mask(labels)
    # Add the detection probabilitiy to each feature (same indexing as the polys since it orginates from the segmentation mask indices in both cases)
    probs = list(polys["prob"])
    for prob, feature in zip(probs, features):
        feature.properties.update({
            "Detection probability": float(prob)
        })
        # [Notes for QuPath extension]
        # Can add measurements in QuPath similarly to the "Detection probability" (values should be a number - not a string)
        # Can set a classification in QuPath by adding a "Classification" key with a string value (can be "Positive"/"Negative"/"1+"/"2+"/"3+" or anything else)

    return {"mask": labels, "features": features}
