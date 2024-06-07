# API Python algos

## Description

The API Python algos is a Python API that aims to enable users access to Python-based image processing algorithms
from other software.
In particular, the API can be used to run Python-based image processing algorithms in QuPath with the extension
[qupath-extension-pyalgos](https://github.com/EPFL-Center-for-Imaging/qupath-extension-pyalogs),
and in Fiji with the plugin [ij-plugin-pyalgos](https://github.com/EPFL-Center-for-Imaging/ij-plugin-pyalgos).

## Setup

1. Create a Python 3.9-3.11 virtual environment and activate it
2. Install the required python packages for the app:
   `pip install -r requirements.txt`
3. Then install the additional required packages for the implemented algorithms. For the already implemented algorithm *Stardist*,
   follow the instructions from [here](https://github.com/stardist/stardist?tab=readme-ov-file#installation).
   To add new algorithms, see [Adding new algorithms](#adding-new-algorithms).

## Usage

To launch the server on local host and port 8000:
```python -m uvicorn app.main:app --host 127.0.0.1 --port 8000```

Once the server is launched, there is an interactive API doc available on http://127.0.0.1:8000/redoc .

## Algorithms

The image processing algorithms should take as input an image (`numpy.ndarray`) and a set of parameters (`**kwargs`).
The output is a dictionary, where the keys match specfic endpoints to access the result in the API, mainly "image"
and/or "features".
In the Fiji plugin, it is the resulting image that is displayed, in the QuPath extension, it is the resulting features (
with associated measurements and classifications)
that are displayed.

### Implemented algorithms

#### example

The example algorithm is added to showcase the functionalities of the API and the related plugin and extension.
It shows the different types of parameters that can be used, and all the available endpoints for the result.

#### stardist

An algorithm is implemented as an example: *[Stardist](https://github.com/stardist/stardist) - Object Detection with
Star-convex Shapes*.
The outputs of the algorithm consist in the segmentation mask and a list of the geojson.Feature for each detected
object.
Using the Fiji plug-in, the mask is displayed in a new window in Fiji.
Using the QuPath extension, the features are displayed as detection objects on the input image in QuPath.

- Uwe Schmidt, Martin Weigert, Coleman Broaddus, and Gene Myers,
  [*Cell Detection with Star-convex Polygons*](https://arxiv.org/abs/1806.03535).
  International Conference on Medical Image Computing and Computer-Assisted Intervention (MICCAI), Granada, Spain,
  September 2018.

- Martin Weigert, Uwe Schmidt, Robert Haase, Ko Sugawara, and Gene Myers,
  [*Star-convex Polyhedra for 3D Object Detection and Segmentation in
  Microscopy*](http://openaccess.thecvf.com/content_WACV_2020/papers/Weigert_Star-convex_Polyhedra_for_3D_Object_Detection_and_Segmentation_in_Microscopy_WACV_2020_paper.pdf),
  The IEEE Winter Conference on Applications of Computer Vision (WACV), Snowmass Village, Colorado, March 2020.

### Adding new algorithms

Algorithms can be implemented and added in the **algos** package to be used with the app.
To do so:

1. Implement a new algorithm in the **algos** package. Encapsulate it into a single function, taking as input an image
   (`numpy.ndarray`) and `**kwargs`.
   The return type should be a dictionary with the keys matching available endpoints, e.g. the ```run_example()```
   method return a dictionary with `image` and  `features` keys.
   Note that there are some helpful methods in algos/computes_features.py to compute features from a segmentation mask.
2. To add info visible to the client about the implemented algorithm, add a new entry in the **algos/algo_def.py** file.
   The entry should contain:
    - a unique *id* number,
    - a unique *name*,
    - a *description*,
    - specifications about *input_data_format*,
    - the list of *required_parameters*: each specifying a "name", "display_name", "description", "type", "
      default_value" or "values" if the type is a list.
      The required parameters relate to the keyword arguments of the algorithm's method, and
      the *name* should match exactly the argument name.
      The *display_name* is used for display in the UI of the extension/plug-in and the *description* can be displayed
      as a
      hint text when hovering over the *display_name*.
      The *type* is useful for conversion to the correct type in Java. The *default_value* will be the one used if
      no input from the client is given, and it is the value displayed by default in the UI.
    - the "output_endpoints" should match the keys of the output dictionary of the algorithm method, and should match
      the available endpoints of the API to get the result, currently "image" or "features".
3. Lastly, to link the definition of the algorithm with its implemented function,
   add an entry to the ALGOS_MAP in **algos/algo_map.py**, where the key is the name specified
   in **algos/algo_def.py** (from step 2) and the value is the implemented function (from step 1).

## Tests

To run the tests: ```python -m pytest```
