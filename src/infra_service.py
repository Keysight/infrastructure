if __package__ is None or __package__ == "":
    from generated import infra_pb2, infra_pb2_grpc
else:
    from .generated import infra_pb2, infra_pb2_grpc

class InfraService():
    @staticmethod
    def Validate(request: infra_pb2.ValidationRequest):
        """Validate every connection in Device and Infrastructure.

        Every Device in Infrastructure.inventory.devices has connections which
        must have a valid number of pieces separated by a ".".

        The names in the following connection breakdown must be present in the
        Device components and links.

        The format of a Device connection is the following:
        "component_name.component_index.link_name.component_name.component_index"
        """
        validation_response = infra_pb2.ValidationResponse()
        for name, device in request.infrastructure.inventory.devices.items():
            if name != device.name:
                validation_response.inva
            for connection in device.connections:
        return validation_response