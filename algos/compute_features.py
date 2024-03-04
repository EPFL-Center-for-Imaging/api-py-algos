import geojson
import numpy as np
from geojson import Feature
from geojson import Polygon as geojson_polygon
from skimage import measure


def get_features_from_segm_mask(segm_mask: np.ndarray) -> [geojson.Feature]:
    """
    Args:
        segm_mask: Segmentation mask with the background pixels set to zero and the pixels assigned to a segmented
         object set to an int value

    Returns:
        A list containing the contours of each object as a geojson.Feature
    """
    features = []
    indices = np.unique(segm_mask)
    indices = np.delete(indices, indices == 0)  # remove background
    if indices.size > 0:
        for i in indices.tolist():
            geom = _mask_to_geometry(np.asarray(segm_mask == i))
            features.append(Feature(geometry=geom, properties={"Detection ID": i}))
    return features


def _mask_to_geometry(mask: np.ndarray) -> geojson.Polygon:
    """
    Adapted from ksugar's samapi https://github.com/ksugar/samapi/blob/3c93d64497051ebb34ddeacd47153313bf31a5b5/src/samapi/utils.py#L16
    which is modified from https://github.com/MouseLand/cellpose_web/blob/main/utils.py
    Args:
        mask: Binary mask with background pixels = 0 & single object pixels = 1
    Returns:
        The contour of the object as a geojson.Polygon (if there is more than one object in the mask,
         the geometry of the largest one is returned)
    """
    # ensure the mask is binary for correct contours finding & handle objects at the edges properly by zero-padding
    mask = np.pad(mask > 0, 1)
    contours_find = measure.find_contours(mask, 0.5)
    if len(contours_find) == 1:
        index = 0
    else:
        # if more than one contour is found, the largest one is returned
        n_pixels = []
        for _, item in enumerate(contours_find):
            n_pixels.append(len(item))
        index = np.argmax(n_pixels)
    contour = contours_find[index]
    contour -= 1  # reset padding
    contour_as_numpy = contour[:, np.argsort([1, 0])]  # sort for correct x-y convention
    return geojson_polygon([contour_as_numpy.tolist()])
