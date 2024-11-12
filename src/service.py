"""Service class that can be used without the need for a grpc service and grpc
client.

"""

if __package__ is None or __package__ == "":
    from generated.service_pb2 import ValidationRequest, ValidationError, ValidationResponse
else:
    from .generated.service_pb2 import ValidationRequest, ValidationError, ValidationResponse


class Service:
    def __init__(self):
        self._validation_request = None
        self._validation_response = None

    def _validate_presence(self, object, name):
        if object.HasField(name) is False:
            self._validation_response.errors.append(
                ValidationError(optional=f"{object.DESCRIPTOR.name} {name} field has not been set")
            )

    def _validate_map(self, map):
        for key, object in map.items():
            if object.name != key:
                self._validation_response.errors.append(
                    ValidationError(
                        map=f"{object.DESCRIPTOR.name} name value:{object.name} does not match map key:{key}'"
                    )
                )

    def _validate_component_connection(self, device, connection: str):
        try:
            c1, c1_idx, link, c2, c2_idx = connection.split(".")
            self._validate_component(device, c1, c1_idx)
            self._validate_component(device, c2, c2_idx)
            self._validate_link_name(device, link)
        except ValueError:
            self._validation_response.errors.append(
                ValidationError(
                    referential_integrity=f"Infrastructure.devices[{device.name}].connections:[{connection}] is incorrectly formatted"
                )
            )

    def _validate_component(self, device, name, index):
        if name not in device.components:
            self._validation_response.errors.append(
                ValidationError(
                    referential_integrity=f"Infrastructure.devices[{device.name}].components[{name}] does not exist"
                )
            )
        try:
            index = int(index)
            if index < 0 or index > device.components[name].count - 1:
                self._validation_response.errors.append(
                    ValidationError(
                        referential_integrity=f"Component:{name} index:{index} must be >= 0 and <{device.components[name].count}"
                    )
                )
        except ValueError:
            self._validation_response.errors.append(
                ValidationError(referential_integrity=f"Index:{index} must be a valid integer")
            )

    def _validate_link_name(self, device, name: str):
        if name not in device.links:
            self._validation_response.errors.append(
                ValidationError(
                    referential_integrity=f"Infrastructure.devices[{device.name}].links[{name}] does not exist"
                )
            )

    def _validate_oneof(self, object, name):
        if object.WhichOneof(name) is None:
            self._validation_response.errors.append(
                ValidationError(oneof=f"{object.DESCRIPTOR.name} oneof:{name} must be set")
            )

    def validate(self, request: ValidationRequest):
        """Validate Infrastructure and Bindings.

        Enforces the correctness of messages by validating presence, maps,
        oneof and referential integrity that is implied in device/infrastructure
        connection paths and binding infrastructure paths.

        Every Device in Infrastructure.inventory.devices has connections which
        must have a valid number of pieces separated by a ".".

        Every connection in Infrastructure.connections must be composed of
        a valid number of pieces separated by a "." and the pieces must exist
        in the Infrastructure.inventory.devices and Infrastructure.inventory.links.

        The format of a Device connection is the following:
        "component_name.component_index.link_name.component_name.component_index"
        """
        self._validation_request = request
        self._validation_response = ValidationResponse()

        self._validate_map(request.infrastructure.inventory.devices)
        for device in request.infrastructure.inventory.devices.values():
            self._validate_presence(device, "name")
            self._validate_map(device.links)
            self._validate_map(device.components)
            for link in device.links.values():
                self._validate_presence(link, "name")
            for component in device.components.values():
                self._validate_presence(component, "name")
                self._validate_presence(component, "count")
            for connection in device.connections:
                self._validate_component_connection(device, connection)
            for link in device.links.values():
                self._validate_oneof(link.bandwidth, "type")
        return self._validation_response
