# API Python algos

## Setup

1. Create a Python 3.10 virtual environment (for Linux: `python -m venv path/to/venv_pyalgos`)
2. Activate the virtual environment (for Linux: `source path/to/venv_pyalgos/bin/activate`)
3. Install the required python packages for the app:
`pip install -r requirements.txt`
4. Then install the required packages for the selected algorithms, e.g. for stardist, follow the instructions from 
[here](https://github.com/stardist/stardist?tab=readme-ov-file#installation).


## Usage

To launch the server on port 8000: 
```python -m uvicorn app.main:app --reload --port 8000```

Once the server is launched, there is an interactive API doc available, e.g. if the server is launched on local host with port 8000:
http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc .

To list processes using a specific port, e.g. port 8000: `lsof -i :8000`.

## Tests
To run the tests: ```python -m pytest```
