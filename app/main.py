import traceback
import warnings

import matplotlib.pyplot as plt
import numpy as np
from fastapi import FastAPI, HTTPException
from geojson import Feature
from pydantic import BaseModel

from algos import (AVAILABLE_ALGOS, get_required_algo_params, get_algo_info, get_algo_method)
from app.encoding import encode_image, decode_image
from app.features import get_features_from_segm_mask

app = FastAPI(title="Python algos app",
              version="0.1.0")


class Dimensions(BaseModel):
    width: int
    height: int
    channels: int | None = None
    depth: int | None = None
    frames: int | None = None


class ImageData(BaseModel):
    data: str


class Parameters(BaseModel):
    parameters: dict | None = None


class Message(BaseModel):
    message: str


class ServerData:
    """ Class containing the data on the server side """

    def __init__(self):
        self._selected_algo = None
        self._algo_params = {}
        self._image_array = None
        self._result_array = None
        self._result_features = []

    @property
    def selected_algo_name(self) -> str | None:
        return self._selected_algo

    @selected_algo_name.setter
    def selected_algo_name(self, algo: str):
        if algo in available_algo_names:
            self._selected_algo = algo
        else:
            self._selected_algo = None
            raise ValueError(algo)

    @property
    def algo_params(self) -> {}:
        return self._algo_params

    @algo_params.setter
    def algo_params(self, params: {}):
        if _check_algo_params(self.selected_algo_name, params):
            self._algo_params = params
        else:
            self._algo_params = {}
            raise ValueError(params)

    @property
    def image_array(self) -> np.ndarray | None:
        return self._image_array

    @image_array.setter
    def image_array(self, data: np.ndarray):
        self._image_array = data

    @property
    def result_array(self) -> np.ndarray | None:
        return self._result_array

    @result_array.setter
    def result_array(self, res: np.ndarray):
        self._result_array = res

    @property
    def result_features(self) -> []:
        return self._result_features

    @result_features.setter
    def result_features(self, feats: [Feature]):
        self._result_features = feats

    def clear_all(self):
        self._selected_algo = None
        self._algo_params = {}
        self._image_array = None
        self._result_array = None
        self._result_features = []


# Available algos names & required parameters
available_algo_names = [algo["name"] for algo in AVAILABLE_ALGOS]

server_data = ServerData()


@app.get("/")
def welcome() -> {}:
    return {"message": "hello"}


@app.get("/image/{algo_name}/parameters")
def get_selected_algo_params(algo_name: str):
    """ Get the algorithm parameters by the user for the given algo_name """
    if server_data.selected_algo_name != algo_name:
        raise HTTPException(404)
    return server_data.algo_params


@app.post("/image/{algo_name}/parameters")
def set_algo_params(algo_name: str, params: Parameters) -> {}:
    """ Set the parameters for the algo_name """
    try:
        server_data.selected_algo_name = algo_name
    except ValueError:
        raise HTTPException(400, f"Unknown algorithm {algo_name}")
    try:
        server_data.algo_params = params.parameters
    except ValueError:
        raise HTTPException(400, f"Incorrect algorithm parameters for {algo_name}")
    return server_data.algo_params


def _check_algo_params(algo_name: str, input_algo_params: {}) -> bool:
    # TODO: Replace warnings with HTTPException ?
    """ Check that the input_algo_params contain all the required algo parameters for the given algo_name
    Returns True if all the required parameters are set """
    if algo_name not in available_algo_names:
        warnings.warn(f"Unknown algorithm {algo_name}")
        return False

    # Check that each required parameter is contained in the input parameters
    rqd_algo_params = get_required_algo_params(algo_name)
    if not rqd_algo_params:
        return True
    rqd_algo_params_names = [param.get("name") for param in rqd_algo_params]
    if not input_algo_params:
        return False
    for param_name in rqd_algo_params_names:
        if not input_algo_params.get(param_name):
            return False
    return True


def _run_algo(algo_method, data: np.ndarray, **algo_parameters) -> {} or None:
    """ Run the given algo_method for the data with the algo_parameters """
    try:
        result = algo_method(data, **algo_parameters)
        return result
    except Exception:
        traceback.print_exc()
        return None


@app.get("/algos_names/")
def read_algos_names() -> {}:
    """ Get the available algo names"""
    response = {'algos_names': available_algo_names}
    return response


@app.get("/algos/{algo_name}/")
def read_algo_info(algo_name: str):
    """ Get all the information for the given algo_name """
    if algo_name not in available_algo_names:
        raise HTTPException(status_code=404, detail=f"Algorithm {algo_name} not found")
    algo_info = get_algo_info(algo_name)
    return algo_info


@app.get("/algos/{algo_name}/required_parameters")
def read_algo_params(algo_name: str):
    """ Get the required parameters for the given algo_name """
    if algo_name not in available_algo_names:
        raise HTTPException(status_code=404, detail=f"Algorithm {algo_name} not found")
    rqd_algo_params = get_required_algo_params(algo_name)
    return {"parameters": rqd_algo_params}


@app.post("/image/{algo_name}/result")
def process_data(algo_name: str):
    """ Process the image data with the given algo_name (the image data should be set &
    the algo parameters should be set) """
    if algo_name not in available_algo_names:
        raise HTTPException(status_code=404, detail=f"Algorithm {algo_name} not found")
    algo_method = get_algo_method(server_data.selected_algo_name)
    if algo_method is None:
        raise HTTPException(status_code=404, detail=f"Algorithm implementation for {algo_name} not found")
    if not _check_algo_params(algo_name, server_data.algo_params):
        raise HTTPException(status_code=400, detail=f"Incorrect algorithm parameters for {algo_name}")

    server_data.result_array = _run_algo(algo_method, server_data.image_array, **server_data.algo_params)
    if server_data.result_array is None:
        raise HTTPException(500)
    server_data.result_features = get_features_from_segm_mask(server_data.result_array)


@app.delete("/image")
def delete_image():
    """ Delete all the information related to the image & result on the server """
    server_data.clear_all()


@app.post("/image")
async def send_image(image: ImageData):
    """ Send the image as a Base64 encoded string & save the decoded np.ndarray to the ServerData """
    try:
        server_data.image_array = decode_image(image.data)
    except ValueError as e:
        raise HTTPException(415, e)  # Unsupported Media Type


@app.get("/image/{algo_name}/result")
async def get_result_image(algo_name: str) -> {}:
    """ Get the computed result of the image processing with the given algo_name
    as an image in a Base64 encoded string """
    if server_data.selected_algo_name != algo_name:
        raise HTTPException(404)
    if server_data.result_array is None:
        raise HTTPException(404)
    return {"data": encode_image(server_data.result_array)}


@app.get("/image/{algo_name}/result_geojson")
async def get_result_geojson(algo_name: str) -> {}:
    """ Get the computed result of the image processing with the given algo_name
    as a list of geojson.Feature """
    if server_data.selected_algo_name != algo_name:
        raise HTTPException(404)
    if server_data.result_array is None:
        raise HTTPException(404)
    return {"features": server_data.result_features}


def save_result_plot():
    """ Plot of the original image and its computed result - to check result on server side """
    plt.figure()
    plt.suptitle("SERVER")
    plt.subplot(1, 2, 1)
    if server_data.image_array is not None:
        plt.imshow(server_data.image_array)
    plt.subplot(1, 2, 2)
    if server_data.result_array is not None:
        plt.imshow(server_data.result_array)
    plt.savefig("result.png")
    plt.close()
