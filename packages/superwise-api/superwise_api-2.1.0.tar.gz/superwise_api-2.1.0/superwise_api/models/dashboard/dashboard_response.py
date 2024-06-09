from __future__ import annotations

import re  # noqa: F401

from superwise_api.client.models.dashboard import Dashboard as RawDashboard


class Dashboard(RawDashboard):
    """
    Dashboard
    """

    @classmethod
    def from_dict(cls, obj: dict) -> Dashboard:
        """Create an instance of Dashboard from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Dashboard.parse_obj(obj)

        _obj = Dashboard.parse_obj(
            {
                "id": obj.get("id"),
                "name": obj.get("name"),
                "created_by": obj.get("created_by"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "positions": obj.get("positions"),
            }
        )
        return _obj
