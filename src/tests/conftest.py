import sys
import os

for directory_piece in ["..", "generated", "tests"]:
    sys.path.append(os.path.join(os.path.dirname(__file__), directory_piece))

import pytest
from keysight_chakra.generated.infra_pb2 import Device, Component, Link, LinkType, Bandwidth, Npu, Nic
from service import Service


@pytest.fixture
def service() -> Service:
    return Service()


@pytest.fixture
def host() -> Device:
    device = Device(
        name="aic-sb203-lx",
        components={
            "tesla-t4": Component(name="tesla-t4", count=1, npu=Npu()),
            "cx6": Component(name="cx6", count=1, nic=Nic()),
        },
        links={"pcie-3": Link(name="pcie-3", type=LinkType.LINK_PCIE, bandwidth=Bandwidth(gbps=32))},
        connections=["tesla-t4.0.pcie-3.cx6.0"],
    )
    return device
