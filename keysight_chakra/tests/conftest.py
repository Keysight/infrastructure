import sys
import os

for directory_piece in ["../.."]:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), directory_piece)))

print(sys.path)

import pytest
from keysight_chakra.protobuf.infra_pb2 import Device, Component, Link, Bandwidth, Npu, Nic
from keysight_chakra.validation import Validation


@pytest.fixture
def validation() -> Validation:
    return Validation()


@pytest.fixture
def host() -> Device:
    device = Device(
        name="aic-sb203-lx",
        components={
            "tesla-t4": Component(name="tesla-t4", count=1, npu=Npu()),
            "cx6": Component(name="cx6", count=1, nic=Nic()),
        },
        links={"pcie-3": Link(name="pcie-3", bandwidth=Bandwidth(gbps=32))},
        connections=["tesla-t4.0.pcie-3.cx6.0"],
    )
    return device
