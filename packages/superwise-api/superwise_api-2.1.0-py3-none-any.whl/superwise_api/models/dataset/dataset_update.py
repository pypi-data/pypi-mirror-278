from typing import Optional

from pydantic import Field

from superwise_api.client import SchemaUpdate
from superwise_api.client.models.dataset_update import DatasetUpdate as RawDatasetUpdate


class DatasetUpdate(RawDatasetUpdate):
    name: Optional[str] = None
    description: Optional[str] = None
    id: Optional[str] = None
    var_schema: Optional[SchemaUpdate] = Field(None, alias="schema")
