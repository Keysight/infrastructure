if __package__ is None or __package__ == "":
    from generated.service_pb2 import ValidationRequest, ValidationError, ValidationResponse
else:
    from .generated.service_pb2 import ValidationRequest, ValidationError, ValidationResponse


class Service:
    @staticmethod
    def Validate(request: ValidationRequest):
        """Validate every connection in the Infrastructure.

        Every Device in Infrastructure.inventory.devices has connections which
        must have a valid number of pieces separated by a ".".

        Every connection in Infrastructure.connections must be composed of
        a valid number of pieces separated by a "." and the pieces must exist
        in the Infrastructure.inventory.devices and Infrastructure.inventory.links.

        The format of a Device connection is the following:
        "component_name.component_index.link_name.component_name.component_index"
        """
        errors = []
        for device_key, device in request.infrastructure.inventory.devices.items():
            if device.HasField("name") is False:
                errors.append(ValidationError(optional=f"Device name field has not been set"))
            if device_key != device.name:
                errors.append(
                    ValidationError(
                        map=f"Device key '{device_key}' does not match Device.name '{device.name}'"
                    )
                )
            for link_key, link in device.links.items():
                if link_key != link.name:
                    errors.append(
                        ValidationError(
                            map=f"Device '{device.name}' link key '{link_key}' does not match Link.name '{link.name}'"
                        )
                    )
                if link.bandwidth.WhichOneof("type") is None:
                    errors.append(ValidationError(oneof="Device.links.bandwidth type must be set"))
            for connection in device.connections:
                try:
                    src, src_idx, link, dst, dst_idx = connection.split(".")
                except ValueError:
                    errors.append(
                        ValidationError(
                            connection=f"Component connection in device '{device.name}' is incorrectly formatted"
                        )
                    )
        return ValidationResponse(errors=errors)
