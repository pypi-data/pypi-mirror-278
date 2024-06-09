from typing import Optional

from pydantic import conlist
from pydantic import Field

from superwise_api.client.models.page_dataset_response import PageDatasetResponse as RawPageDatasetResponse
from superwise_api.models.dataset.dataset_response import DatasetResponse


class PageDatasetResponse(RawPageDatasetResponse):
    items: conlist(DatasetResponse) = Field(...)

    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[PageDatasetResponse]":
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PageDatasetResponse.parse_obj(obj)

        _obj = PageDatasetResponse.parse_obj(
            {
                "items": [DatasetResponse.from_dict(_item) for _item in obj.get("items")]
                if obj.get("items") is not None
                else None,
                "total": obj.get("total") if obj.get("total") is not None else 0,
                "page": obj.get("page"),
                "size": obj.get("size"),
                "next": obj.get("next"),
                "previous": obj.get("previous"),
                "first": obj.get("first"),
                "last": obj.get("last"),
            }
        )
        return _obj
