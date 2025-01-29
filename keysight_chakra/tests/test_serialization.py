import pytest
from google.protobuf.json_format import MessageToJson, Parse
from google.protobuf.any_pb2 import Any
from google.protobuf.wrappers_pb2 import StringValue
from keysight_chakra.generated.annotate_pb2 import Annotation, Target, Data


class AnyString:
    """Wrapper class for StringValue and Any"""

    TYPE = "type.googleapis.com/google.protobuf.StringValue"

    @staticmethod
    def get_any(value: str) -> Any:
        """Returns an Any message with the string encapsulated using StringValue"""
        assert isinstance(value, str)
        any: Any = Any()
        any.Pack(StringValue(value=value))
        return any

    def get_str(any: Any) -> str:
        """Returns a str from an Any message"""
        assert isinstance(any, Any)
        assert any.type_url == AnyString.TYPE
        string_value = StringValue()
        any.Unpack(string_value)
        return string_value.value


def test_string_serialization():
    """Test serialization of Any string values in protobuf messages to json
    and from json.
    """
    annotation_value = "3 Tier Clos Fabric Infrastructure"

    annotation1 = Annotation(
        targets=[Target(infrastructure="Infrastructure Description")],
        data=Data(
            name="Description",
            value=AnyString.get_any(annotation_value),
        ),
    )

    serialized_json = MessageToJson(
        annotation1,
        including_default_value_fields=True,
    )

    annotation2 = Annotation()
    Parse(serialized_json, annotation2)

    for target1, target2 in zip(annotation1.targets, annotation2.targets):
        assert target1.infrastructure == target2.infrastructure

    annotation1_value = AnyString.get_str(annotation1.data.value)
    annotation2_value = AnyString.get_str(annotation2.data.value)
    assert annotation1_value == annotation2_value == annotation_value


if __name__ == "__main__":
    pytest.main(["-s", "-o", "log_cli=True", "-o", "log_cli_level=INFO", __file__])
