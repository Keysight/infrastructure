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

def test_generic_host_with_params():
    host = GenericHost(npu_count=4, nvlink_bandwidth_gbps=600)
    assert "nvlink" in host._device.links
    assert host._device.links["nvlink"].type == infra.LINK_NVLINK
    seen_pair_map = {
        "0_1": False,
        "0_2": False,
        "0_3": False,
        "1_2": False,
        "1_3": False,
        "2_3": False,
    }
    for connection in host._device.connections:
        if connection.link.c1 == "npu" and connection.link.c2 == "npu":
            pair_key = f"{connection.link.c1_index}_{connection.link.c2_index}"
            assert pair_key in seen_pair_map
            assert not seen_pair_map[pair_key]
            seen_pair_map[pair_key] = True
    for v in seen_pair_map.values():
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
