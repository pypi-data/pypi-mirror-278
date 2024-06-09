from __future__ import annotations

import re  # noqa: F401

from pydantic import conlist
from pydantic import Field

from superwise_api.client.models.page_dashboard import PageDashboard as RawPageDashboard
from superwise_api.models.dashboard.dashboard_response import Dashboard


class PageDashboard(RawPageDashboard):
    """
    PageDashboard
    """

    items: conlist(Dashboard) = Field(...)

    @classmethod
    def from_dict(cls, obj: dict) -> PageDashboard:
        """Create an instance of PageDashboard from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PageDashboard.parse_obj(obj)

        _obj = PageDashboard.parse_obj(
            {
                "items": [Dashboard.from_dict(_item) for _item in obj.get("items")]
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
