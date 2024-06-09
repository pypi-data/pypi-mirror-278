from __future__ import annotations

import re  # noqa: F401

from pydantic import conlist
from pydantic import Field

from superwise_api.client.models import PagePolicyResponse as RawPagePolicyResponse
from superwise_api.models.policy.policy_response import PolicyResponse


class PagePolicyResponse(RawPagePolicyResponse):
    """
    PagePolicyResponse
    """

    items: conlist(PolicyResponse) = Field(...)

    @classmethod
    def from_dict(cls, obj: dict) -> PagePolicyResponse:
        """Create an instance of PagePolicyResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PagePolicyResponse.parse_obj(obj)

        _obj = PagePolicyResponse.parse_obj(
            {
                "items": [PolicyResponse.from_dict(_item) for _item in obj.get("items")]
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
