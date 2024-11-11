import pytest
from service import Service
from generated.service_pb2 import ValidationRequest
from generated.infra_pb2 import Infrastructure, Inventory, Device, Link, LinkType, Bandwidth


def test_valid_device():
    """Test that a device is valid"""
    device = Device(name="host")
    mii = Link(name="mii", type=LinkType.LINK_CUSTOM, bandwidth=Bandwidth(gbps=100))
    device.links[mii.name].CopyFrom(mii)
    inventory = Inventory()
    inventory.devices[device.name].CopyFrom(device)
    infrastructure = Infrastructure(inventory=inventory)
    request = ValidationRequest(infrastructure=infrastructure)
    response = Service.Validate(request=request)
    assert len(response.errors) == 0


def test_missing_bandwidth():
    """Test that a device is missing the bandwidth from a link"""
    device = Device(name="host")
    mii = Link(name="mii", type=LinkType.LINK_CUSTOM)
    device.links[mii.name].CopyFrom(mii)
    inventory = Inventory()
    inventory.devices[device.name].CopyFrom(device)
    infrastructure = Infrastructure(inventory=inventory)
    request = ValidationRequest(infrastructure=infrastructure)
    response = Service.Validate(request=request)
    print(response)
    assert len(response.errors) == 1
    assert response.errors[0].WhichOneof("type") == "oneof"


if __name__ == "__main__":
    pytest.main(["-s", __file__])
