from __future__ import annotations

import re  # noqa: F401
from typing import Any

from superwise_api.client.models.dashboard_item import DashboardItem as RawDashboardItem
from superwise_api.models.dashboard_item.query import Query


class DashboardItem(RawDashboardItem):
    """
    DashboardItem
    """

    query: Query
    item_metadata: Any = None

    @classmethod
    def from_dict(cls, obj: dict) -> DashboardItem:
        """Create an instance of DashboardItem from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DashboardItem.parse_obj(obj)

        _obj = DashboardItem.parse_obj(
            {
                "id": obj.get("id"),
                "name": obj.get("name"),
                "query_type": obj.get("query_type"),
                "datasource": obj.get("datasource"),
                "query": Query.from_dict(obj.get("query")) if obj.get("query") is not None else None,
                "created_by": obj.get("created_by"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "dashboard_id": obj.get("dashboard_id"),
                "item_metadata": obj.get("item_metadata") if obj.get("item_metadata") is not None else None,
            }
        )
        return _obj
