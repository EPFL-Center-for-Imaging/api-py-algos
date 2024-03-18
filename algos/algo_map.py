from typing import Callable

from .stardist_run import run_stardist

# This maps the algo name from algos_def.py to its callable method
ALGOS_MAP = {"stardist": run_stardist}


def get_algo_method(algo_name: str) -> Callable or None:
    """ Return the Callable algo method for the given algo name"""
    return ALGOS_MAP.get(algo_name)
