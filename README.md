# API Python algos

## Setup

1. Create a Python 3.9-3.11 virtual environment and activate it
2. Install the required python packages for the app:
   `pip install -r requirements.txt`
3. Then install the required packages for the implemented algorithms, e.g. for the example algorithm *Stardist*, 
follow the instructions from [here](https://github.com/stardist/stardist?tab=readme-ov-file#installation).

## Usage

To launch the server on local host and port 8000:
```python -m uvicorn app.main:app --port 8000```

Once the server is launched, there is an interactive API doc available, 
e.g. if the server is launched on local host with port 8000:
http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc .


## Algorithms

### Example algorithm

An algorithm is implemented as an example: *[Stardist](https://github.com/stardist/stardist) - Object Detection with Star-convex Shapes*.
The outputs of the algorithm consist in the segmentation mask and a list of the geojson.Feature for each detected object.

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

1. Implement a new algorithm in the algos package. Encapsulate it into a single function, taking as input an image 
    (`np.ndarray`) and `kwargs`.
   The return type should be a dictionary with the keys matching available endpoints, e.g. the ```run_stardist()```
   method return a dictionary with `mask` and  `features` keys, which the client can get from
   */image/stardist/result/mask*
   and */image/stardist/result/features*, respectively.
2. To add info visible to the client about the implemented algorithm, add a new entry in the algos/algo_def.py. The entry
   should contain:

    - a unique "id" number,
    - a unique "name",
    - a "description",
    - specifications about "input_data_format",
    - "required_parameters": each specifying a "name", "display_name", "description", "type", "default_value",
    - "output_endpoints".
3. To be able to run the algorithm on the server, in algos/algo_map.py, add the mapping for the "algo_name" specified
   in algos/algo_def.py to the function defined in step 1.

## Tests

To run the tests: ```python -m pytest```
