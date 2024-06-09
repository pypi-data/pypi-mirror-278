from __future__ import annotations

import re  # noqa: F401

from pydantic import Field

from superwise_api.client.models.policy_response import PolicyResponse as RawPolicyResponse
from superwise_api.models.policy.query import Query


class PolicyResponse(RawPolicyResponse):
    """
    PolicyResponse
    """

    query: Query = Field(...)

    @classmethod
    def from_dict(cls, obj: dict) -> PolicyResponse:
        """Create an instance of PolicyResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PolicyResponse.parse_obj(obj)

        _obj = PolicyResponse.parse_obj(
            {
                "id": obj.get("id"),
                "name": obj.get("name"),
                "created_by": obj.get("created_by"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "last_evaluation": obj.get("last_evaluation"),
                "next_evaluation": obj.get("next_evaluation"),
                "status": obj.get("status"),
                "query": Query.from_dict(obj.get("query")) if obj.get("query") is not None else None,
                "cron_expression": obj.get("cron_expression"),
                "threshold_settings": obj.get("threshold_settings"),
                "destination_ids": obj.get("destination_ids"),
                "alert_on_status": obj.get("alert_on_status"),
                "alert_on_policy_level": obj.get("alert_on_policy_level"),
                "tenant_id": obj.get("tenant_id"),
                "dataset_id": obj.get("dataset_id"),
                "time_range_field": obj.get("time_range_field"),
                "time_range_unit": obj.get("time_range_unit"),
                "time_range_value": obj.get("time_range_value"),
            }
        )
        return _obj
