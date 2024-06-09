from typing import Literal
from typing import Optional
from typing import Union

from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field

from superwise_api.models.tool.enums import EmbeddingModelProvider
from superwise_api.models.tool.enums import GoogleAIEmbeddingModelVersion
from superwise_api.models.tool.enums import OpenAIEmbeddingModelVersion
from superwise_api.models.tool.enums import ToolType


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


class ToolConfigBase(BaseModel):
    type: ToolType


class EmbeddingModelBase(BaseModel):
    provider: EmbeddingModelProvider


class VertexAIModelGardenEmbeddingModel(EmbeddingModelBase):
    provider: Literal[EmbeddingModelProvider.VERTEX_AI_MODEL_GARDEN]
    project_id: str
    endpoint_id: str
    location: str
    service_account: dict[str, str]


class OpenAIEmbeddingModel(EmbeddingModelBase):
    provider: Literal[EmbeddingModelProvider.OPEN_AI]
    version: OpenAIEmbeddingModelVersion
    api_key: str


class GoogleAIEmbeddingModel(EmbeddingModelBase):
    provider: Literal[EmbeddingModelProvider.GOOGLE_AI]
    version: GoogleAIEmbeddingModelVersion
    api_key: str


EmbeddingModel = Union[OpenAIEmbeddingModel, GoogleAIEmbeddingModel, VertexAIModelGardenEmbeddingModel]


class ToolConfigSQLDatabasePostgres(ToolConfigBase):
    type: Literal[ToolType.SQL_DATABASE_POSTGRES]
    connection_string: str = Field(pattern=r"^postgresql://")


class ToolConfigSQLDatabaseMySQL(ToolConfigBase):
    type: Literal[ToolType.SQL_DATABASE_MYSQL]
    connection_string: str = Field(pattern=r"^mysql://")


class ToolConfigSQLDatabaseMSSQL(ToolConfigBase):
    type: Literal[ToolType.SQL_DATABASE_MSSQL]
    connection_string: str = Field(pattern=r"^mssql://")


class ToolConfigSQLDatabaseOracle(ToolConfigBase):
    type: Literal[ToolType.SQL_DATABASE_ORACLE]
    connection_string: str = Field(pattern=r"^oracle://")


class ToolConfigBigQuery(ToolConfigBase):
    type: Literal[ToolType.SQL_DATABASE_BIGQUERY]
    project_id: str
    dataset_id: str
    service_account: dict[str, str]


class ToolConfigPGVector(ToolConfigBase):
    type: Literal[ToolType.PG_VECTOR]
    connection_string: str
    table_name: str
    embedding_model: EmbeddingModel = Field(..., discriminator="provider")


class ToolConfigPineconeVectorDB(ToolConfigBase):
    type: Literal[ToolType.PINECONE_VECTOR_DB]
    api_key: str
    index_name: str
    embedding_model: EmbeddingModel = Field(..., discriminator="provider")


class BearerAuthenticationConfig(BaseModel):
    type: Literal["Bearer"]
    token: str


# can add more types of authentication here like OAuth2
AuthenticationConfig = BearerAuthenticationConfig


class ToolConfigOpenAPI(ToolConfigBase):
    type: Literal[ToolType.OPENAPI]
    openapi_schema: dict
    authentication: Optional[AuthenticationConfig] = None


ToolConfig = Union[
    ToolConfigPGVector,
    ToolConfigPineconeVectorDB,
    ToolConfigSQLDatabasePostgres,
    ToolConfigSQLDatabaseMySQL,
    ToolConfigSQLDatabaseMSSQL,
    ToolConfigSQLDatabaseOracle,
    ToolConfigBigQuery,
    ToolConfigOpenAPI,
]


class ToolDef(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)
    config: ToolConfig
