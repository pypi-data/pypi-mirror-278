from enum import Enum


class ToolType(str, Enum):
    PINECONE_VECTOR_DB = "PineconeVectorDB"
    PG_VECTOR = "PGVector"
    SQL_DATABASE_POSTGRES = "PostgreSQL"
    SQL_DATABASE_BIGQUERY = "BigQuery"
    SQL_DATABASE_MYSQL = "MySQL"
    SQL_DATABASE_MSSQL = "MSSQL"
    SQL_DATABASE_ORACLE = "Oracle"
    OPENAPI = "OpenAPI"


class EmbeddingModelProvider(str, Enum):
    VERTEX_AI_MODEL_GARDEN = "VertexAIModelGarden"
    OPEN_AI = "OpenAI"
    GOOGLE_AI = "GoogleAI"


class OpenAIEmbeddingModelVersion(str, Enum):
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"


class GoogleAIEmbeddingModelVersion(str, Enum):
    EMBEDDING_V1 = "models/embedding-001"
