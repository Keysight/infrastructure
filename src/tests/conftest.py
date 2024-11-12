import pytest
import os
import sys

sys.path.extend(
    [
        os.path.join(os.path.dirname(__file__), ".."),
        os.path.join(os.path.dirname(__file__), "../generated"),
    ]
)

from infra_pb2 import Device


@pytest.fixture
def device():
    host = Device(name="host")
    return host
