from typing import Optional

from superwise_api.client.models.model_schema import ModelSchema


class DatasetSchema(ModelSchema):
    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[DatasetSchema]":
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ModelSchema.parse_obj(obj)

        _obj = ModelSchema.parse_obj(
            {
                "key_field": obj.get("key_field"),
                "timestamp_partition_field": obj.get("timestamp_partition_field"),
                "fields": obj.get("fields"),
            }
        )
        return _obj
