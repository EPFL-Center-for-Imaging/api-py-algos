import pytest
from fastapi.testclient import TestClient

from app.main import *

client = TestClient(app)


@pytest.fixture()
def selected_algo_name():
    return "example"


def test_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}


def test_example_algo_info(selected_algo_name):
    algos_name_json = get_available_algos()
    assert "algos_names" in algos_name_json, "Missing 'algos_names' key from JSON response of available algos"
    algos_names = algos_name_json.get("algos_names")
    assert selected_algo_name in algos_names, "Example algorithm not found in list of available algorithms"

    algo_info_json = get_algo_info(selected_algo_name)
    assert "description" in algo_info_json, "Missing 'description' key from JSON response of algorithm info"
    assert algo_info_json.get("description") == "Description for example algorithm", \
        "Unexpected 'description' for example algo"


def test_unknown_algo_raises_exc():
    with pytest.raises(HTTPException) as exc_info:
        read_algo_info("ghost")
    assert exc_info.value.status_code == 404

# TODO: Add tests with example algorithm
