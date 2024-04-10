import numpy as np
from csbdeep.utils import normalize
from stardist.models import StarDist2D

from .compute_features import get_features_from_segm_mask


def run_stardist(data: np.ndarray, **kwargs) -> {}:
    if not isinstance(data, np.ndarray):
        raise TypeError(type(data))

    model_name = kwargs.get("model_name")
    if model_name == "2D_versatile_he":
        assert data.ndim == 3 and data.shape[2] == 3, \
            f"Expecting 2D RGB image for predictions using the '{model_name}' model"
    elif model_name == "2D_versatile_fluo":
        assert data.ndim == 2, \
            f"Expecting 2D single-channel image for predictions using the '{model_name}' model"
    model = StarDist2D.from_pretrained(model_name)
    kwargs.pop("model_name")

    block_size = kwargs.get("block_size")
    if (data.shape[0] > block_size) or (data.shape[1] > block_size):
        if data.ndim == 2:
            axes = "YX"
        elif data.ndim == 3:
            axes = "YXC"
        else:
            raise ValueError(f"Unexpected image dimensions: {data.ndim}")
        labels, polys = model.predict_instances_big(normalize(data), axes=axes, **kwargs)
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
