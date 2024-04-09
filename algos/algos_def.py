AVAILABLE_ALGOS = [
    {"id": 1, "name": "stardist", "description": "Object detection with star-convex shapes",
     "input_data_format": {"type": "2D image", "ndim": 2},
     "required_parameters": [
         {"name": "model_name", "display_name": "Model",
          "description": "Pretrained stardist model name",
          "type": "list", "values": ["2D_versatile_he", "2D_versatile_fluo"]},
         {"name": "prob_thresh", "display_name": "Probability threshold",
          "description": "Consider only object candidates from pixels with predicted object probability above this threshold",
          "type": "float", "default_value": 0.5},
         {"name": "nms_thresh", "display_name": "Overlap threshold",
          "description": "Perform non-maximum suppression that considers two objects to be the same when their area/surface overlap exceeds this threshold",
          "type": "float", "default_value": 0.4},
         {"name": "scale", "display_name": "Scale",
          "description": "Scale the input image internally by this factor and rescale the output accordingly (<1 to downsample, >1 to upsample)",
          "type": "float", "default_value": 1.0},
         {"name": "block_size", "display_name": "Tile size",
          "description": "Process input image in tiles of the provided shape",
          "type": "int", "default_value": 2048},
         {"name": "min_overlap", "display_name": "Tile overlap",
          "description": "Amount of guaranteed overlap between tiles (All predicted object instances should be smaller than this value!)",
          "type": "int", "default_value": 128}
     ],
     "output_endpoints": ["mask", "features"]
     }
]


def get_required_algo_params(algo_name: str) -> []:
    """ Get the list of required algo parameters for the given algo_name """
    for algo in AVAILABLE_ALGOS:
        if algo.get("name") == algo_name:
            required_params = algo.get("required_parameters")
            return required_params if required_params else []
    return []


def get_input_dataformat(algo_name: str) -> {}:
    """ Get information about the expected input data format for the given algo_name """
    for algo in AVAILABLE_ALGOS:
        if algo.get("name") == algo_name:
            input_data_format = algo.get("input_data_format")
            return input_data_format if input_data_format else {}
    return {}


def get_algo_info(algo_name: str) -> {}:
    """ Get information about the given algo_name """
    for algo in AVAILABLE_ALGOS:
        if algo.get("name") == algo_name:
            return algo
    return {}
