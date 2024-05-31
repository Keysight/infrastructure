import pytest
from keysight_chakra.generic import GenericHost
from keysight_chakra.closfabric import ClosFabric
from keysight_chakra.zionex import ZionEx
from keysight_chakra.infrastructure import Infrastructure


def test_generic_host():
    host = GenericHost()
    assert host.get_component("npu") is not None
    assert host.get_component("nic") is not None


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
