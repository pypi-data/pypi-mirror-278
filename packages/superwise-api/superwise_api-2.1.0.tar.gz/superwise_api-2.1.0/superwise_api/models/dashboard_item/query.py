from __future__ import annotations

import re  # noqa: F401
from typing import Any
from typing import Optional

from pydantic import conlist

from superwise_api.client.models import DashboardItemQuery as RawQuery
from superwise_api.client.models.dashboard_item_query_order import DashboardItemQueryOrder as Order
from superwise_api.models.dashboard_item.query_filter import QueryFilter as Filter


class Query(RawQuery):
    """
    Query
    """

    order: Optional[Order]
    filters: Optional[conlist(Filter)] = []
    limit: Any = 1000
    time_dimensions: Any = []

    @classmethod
    def from_dict(cls, obj: dict) -> Query:
        """Create an instance of Query from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Query.parse_obj(obj)

        _obj = Query.parse_obj(
            {
                "measures": obj.get("measures"),
                "order": Order.from_dict(obj.get("order")) if obj.get("order") else None,
                "dimensions": obj.get("dimensions"),
                "timezone": obj.get("timezone") if obj.get("timezone") is not None else "UTC",
                "filters": [Filter.from_dict(_item) for _item in obj.get("filters")] if obj.get("filters") else [],
            }
        )
        return _obj
