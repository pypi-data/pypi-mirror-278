from datetime import datetime
from typing import Optional
from typing import Sequence
from typing import Union

from pydantic import BaseModel as PydanticBaseModel
from pydantic import conlist
from pydantic import Field
from pydantic import HttpUrl
from pydantic import UUID4

from superwise_api.client.models.page_application import PageApplication as RawPageApplication
from superwise_api.models.application.enums import GoogleModelVersion
from superwise_api.models.application.enums import ModelProvider
from superwise_api.models.application.enums import OpenAIModelVersion
from superwise_api.models.application.enums import Role
from superwise_api.models.application.enums import VertexAIModelGardenVersion
from superwise_api.models.tool.schemas import ToolDef


class BaseModel(PydanticBaseModel):
    def to_dict(self):
        return self.dict(by_alias=True, exclude_none=False, exclude_unset=True)

    def to_json(self):
        return self.json(by_alias=True, exclude_none=False, exclude_unset=True)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def from_json(cls, json_str):
        return cls.parse_raw(json_str)


class ModelLLM(BaseModel):
    provider: ModelProvider
    version: Union[OpenAIModelVersion, GoogleModelVersion, VertexAIModelGardenVersion]
    api_token: Optional[str]


class Application(BaseModel):
    id: UUID4
    created_by: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    name: str
    llm_model: Optional[ModelLLM] = Field(None, alias="model")
    prompt: Optional[str]
    dataset_id: str
    tools: Sequence[ToolDef]
    url: HttpUrl


class ApplicationConfig(BaseModel):
    llm_model: Optional[ModelLLM] = Field(None, alias="model")
    prompt: Optional[str]
    tools: Sequence[ToolDef]


class ApplicationConfigPayload(ApplicationConfig):
    name: str = Field(..., min_length=1, max_length=95)


class ChatHistoryEntry(BaseModel):
    role: Role = Field(..., description="The role can be either 'human' or 'ai'.")
    message: str = Field(..., description="The message content.")

    class Config:
        json_schema_extra = {"example": {"role": "human", "message": "Tell me about landmarks in Paris."}}


class AskRequestPayload(BaseModel):
    config: ApplicationConfig = Field(..., description="The application configuration.")
    input: str = Field(..., description="The user's current message or question to the AI agent.")
    chat_history: Sequence[ChatHistoryEntry] = Field(
        ..., description="The existing conversation history with the AI agent."
    )


class AskResponsePayload(BaseModel):
    output: str = Field(..., description="The AI agent's response to the user's inquiry.")


class PageApplication(RawPageApplication):
    """
    PageApplication
    """

    items: conlist(Application) = Field(...)
    total: int
    page: int
    size: int

    @classmethod
    def from_dict(cls, obj: dict) -> "PageApplication":
        """Create an instance of PageApplication from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PageApplication.parse_obj(obj)

        _obj = PageApplication.parse_obj(
            {
                "items": [Application.from_dict(_item) for _item in obj.get("items")]
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
