import pytest

from keysight_chakra.generic import GenericHost
from keysight_chakra.closfabric import ClosFabric
from keysight_chakra.zionex import ZionEx
from keysight_chakra.infrastructure import Infrastructure

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/../")
import generated.infra_pb2 as infra


def test_generic_host_no_params():
    host = GenericHost()
    assert host.get_component("npu") is not None
    assert host.get_component("nic") is not None
    assert "npu_interconnect" not in host._device.links

def test_generic_host_with_params():
    npu_count = 4
    host = GenericHost(npu_count=npu_count, npu_interconnect_bandwidth_gbps=600)
    assert "npu_interconnect" in host._device.links
    assert host._device.links["npu_interconnect"].type == infra.LINK_CUSTOM

    seen_map = {}
    for npu_index in range(npu_count):
        seen_map[npu_index] = False

    for connection in host._device.connections:
        if connection.link.c1 == "npu" and connection.link.c2 == "npu_interconnect_switch":
            npu_index = connection.link.c1_index
            assert npu_index in seen_map
            assert not seen_map[npu_index]
            seen_map[npu_index] = True
    for v in seen_map.values():
        assert v == True

@pytest.mark.parametrize(
    "host_devices, rack_capacity, pod_capacity, spine_capacity",
    [
        (8, 4, 1, 0),
        (4, 4, 0, 0),
    ],
)
@pytest.mark.parametrize(
    "over_subscription",
    [(1, 1), (2, 1)],
)
def test_clos_fabric(
    host_devices,
    rack_capacity,
    pod_capacity,
    over_subscription,
    spine_capacity,
):
    """Test creating 2 tier clos fabric"""
    host = GenericHost(npu_count=1)
    clos_fabric = ClosFabric(
        host_device=host,
        host_devices=host_devices,
        rack_capacity=rack_capacity,
        rack_to_pod_oversubscription=over_subscription,
        pod_capacity=pod_capacity,
        spine_capacity=spine_capacity,
    )
    infrastructure = Infrastructure(
        host_device=host,
        host_devices=host_devices,
        fabric=clos_fabric,
        assignment_scheme="ROUND_ROBIN",
    )


def test_zionex_host():
    host = ZionEx()
    assert host.get_component("cpu") is not None
    assert host.get_component("npu") is not None
    assert host.get_component("nic") is not None


if __name__ == "__main__":
    pytest.main(["-s", __file__])
