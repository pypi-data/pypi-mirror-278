from typing import Optional

from pydantic import Field
from pydantic import StrictStr

from superwise_api.client.models import DatasetResponse as RawDatasetResponse
from superwise_api.client.models import DatasetTag
from superwise_api.models.dataset.dataset_schema import DatasetSchema


class DatasetResponse(RawDatasetResponse):
    dataset_schema: Optional[DatasetSchema] = Field(None)
    internal_id: StrictStr = Field(..., alias="_id")

    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[DatasetResponse]":
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DatasetResponse.parse_obj(obj)

        _obj = DatasetResponse.parse_obj(
            {
                "_id": obj.get("_id"),
                "id": obj.get("id"),
                "name": obj.get("name"),
                "description": obj.get("description"),
                "model_version_id": obj.get("model_version_id"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "created_by": obj.get("created_by"),
                "tags": [DatasetTag.from_dict(_item) for _item in obj.get("tags")]
                if obj.get("tags") is not None
                else None,
                "dataset_schema": DatasetSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            }
        )
        return _obj
