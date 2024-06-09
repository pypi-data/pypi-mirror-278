from superwise_api.client import DatasetSourceCreate
from superwise_api.client import DatasetSourcesApi
from superwise_api.client import DatasetSourceUpdate
from superwise_api.errors import raise_exception


class DatasetSource:
    """
        Method | HTTP request | Description
    ------------- | ------------- | -------------
    **create**| **POST** /v1/dataset_sources | Create DatasetSource
    **delete**| **DELETE** /v1/dataset_sources/{dataset_source_id} | Delete DatasetSource
    **get_by_id**| **GET** /v1/dataset_sources/{dataset_source_id} | Get DatasetSource
    **get**| **GET** /v1/dataset_sources | Get DatasetSources
    **update**| **PATCH** /v1/dataset_sources/{dataset_source_id} | Update DatasetSource

    """

    def __init__(self, client):
        self.api = DatasetSourcesApi(client)

    @raise_exception
    def create(self, dataset_source_create: DatasetSourceCreate, **kwargs):
        """
        Create a new DatasetSource.

        - **dataset_id** (str): Required, ID of the dataset. The dataset must already exist.
        - **source_id** (UUID): Required, Unique Identifier(UUID) of the source data. The source must already exist.
        - **folder** (str or None): Optional, Path within the bucket to ingest data from..
        - **query** (str or None): Optional, Query statement to retrieve data.
        - **created_at** (datetime or None): Optional, Timestamp when the data source was created.
        - **updated_at** (datetime or None): Optional, Timestamp when the data source was last updated.
        - **ingest_type** (IngestType): Optional, Type of data ingestion. Default is IngestType.INSERT.
        """
        return self.api.create_dataset_source(dataset_source_create, **kwargs)

    @raise_exception
    def update(self, dataset_source_id, dataset_source_update: DatasetSourceUpdate, **kwargs):
        """
        Update an existing DatasetSource.

        - **id** (str): Optional, ID of the dataset source.
        - **dataset_id** (str): Optional, ID of the dataset. The dataset must already exist.
        - **source_id** (UUID): Optional, Unique Identifier(UUID) of the source data. The source must already exist.
        - **folder** (str or None): Optional, Path within the bucket to ingest data from.
        - **query** (str or None): Optional, Query statement to retrieve data.
        - **ingest_type** (IngestType): Optional, Type of data ingestion. Default is IngestType.INSERT.
        """
        return self.api.update_dataset_source(dataset_source_id, dataset_source_update, **kwargs)

    @raise_exception
    def delete(self, dataset_source_id, **kwargs):
        """
        Delete a specific DatasetSource.

        - **dataset_source_id**: ID of the dataset source
        """
        return self.api.delete_dataset_source(dataset_source_id, **kwargs)

    @raise_exception
    def get_by_id(self, dataset_source_id, **kwargs):
        """
        Retrieve a Dataset Source based on the dataset_source_id.

        - **dataset_source_id**: ID of the dataset source
        """
        return self.api.get_dataset_source(dataset_source_id, **kwargs)

    @raise_exception
    def get(self, **query_params):
        """
        Retrieve all Dataset Sources based on the provided filters.

        - **source_id**: ID of the source
        - **folder**: Path within the bucket to ingest data from
        - **id**: ID of the dataset source
        - **dataset_id**: ID of the dataset
        - **created_by**: Creator of the dataset source
        - **ingest_type**: Type of ingestion
        """
        return self.api.get_dataset_sources(**query_params)
