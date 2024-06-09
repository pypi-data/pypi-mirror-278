from __future__ import annotations

import re  # noqa: F401

from pydantic import conlist
from pydantic import Field

from superwise_api.client.models import PageDashboardItem as RawPageDashboardItem
from superwise_api.models.dashboard_item.dashboard_item_response import DashboardItemResponse


class PageDashboardItem(RawPageDashboardItem):
    """
    PageDashboardItem
    """

    items: conlist(DashboardItemResponse) = Field(...)

    @classmethod
    def from_dict(cls, obj: dict) -> PageDashboardItem:
        """Create an instance of PageDashboardItem from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PageDashboardItem.parse_obj(obj)

        _obj = PageDashboardItem.parse_obj(
            {
                "items": [DashboardItemResponse.from_dict(_item) for _item in obj.get("items")]
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
