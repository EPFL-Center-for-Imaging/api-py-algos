from typing import Callable

from .example_run import run_example
from .stardist_run import run_stardist

# This maps the algo name from its definition in algos_def.py to its Callable method
ALGOS_MAP = {"example": run_example, "stardist": run_stardist}


def get_algo_method(algo_name: str) -> Callable or None:
    """ Return the Callable algo method for the given algo name"""
    return ALGOS_MAP.get(algo_name)
