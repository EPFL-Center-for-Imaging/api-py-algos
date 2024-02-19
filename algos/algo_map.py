from typing import Callable

from .stardist_run import run_stardist


def get_algo_method(algo_name: str) -> Callable or None:
    """ Map the algo_name to its Callable algo method"""
    match algo_name:
        case "stardist":
            return run_stardist
        case _:
            return None
