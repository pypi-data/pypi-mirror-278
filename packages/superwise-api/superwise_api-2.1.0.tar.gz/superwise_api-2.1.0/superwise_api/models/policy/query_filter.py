from __future__ import annotations

import re  # noqa: F401
from typing import Optional
from typing import Union

from pydantic import Field
from pydantic import StrictStr

from superwise_api.client.models.filter import Filter as RawFilter


class QueryFilter(RawFilter):
    """
    Filter
    """

    values: Optional[Union[StrictStr, list[StrictStr]]] = Field(None)

    @classmethod
    def from_dict(cls, obj: dict) -> QueryFilter:
        """Create an instance of Filter from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return QueryFilter.parse_obj(obj)

        _obj = QueryFilter.parse_obj(
            {"member": obj.get("member"), "operator": obj.get("operator"), "values": obj.get("values")}
        )
        return _obj
