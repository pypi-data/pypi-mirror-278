from superwise_api.client import DatasetApi
from superwise_api.client import DatasetCreate
from superwise_api.client import DatasetUpdate
from superwise_api.errors import raise_exception


class Dataset:
    """
        Method | HTTP request | Description
    ------------- | ------------- | -------------
    **create** | **POST** /v1/datasets | Create Dataset
    **delete** | **DELETE** /v1/datasets/{dataset_id} | Delete Dataset
    **get_by_id** | **GET** /v1/datasets/{dataset_id} | Get Dataset
    **get** | **GET** /v1/datasets | Get Datasets
    **search_datasets** | **GET** /v1/datasets/search/{prefix} | Search Datasets
    **update** | **PATCH** /v1/datasets/{dataset_id} | Update Dataset

    """

    def __init__(self, client):
        self.api = DatasetApi(client)

    @raise_exception
    def create(self, dataset_create: DatasetCreate, **kwargs):
        """
        Create a new Dataset

        - **payload** (DatasetCreate): Required. The payload that includes:
            - **name** (str): Name of the dataset, min_length=1, max_length=100.
            - **description** (str or None): A description about the dataset.
            - **id** (str): Unique identifier of the dataset.
            - **model_version_id** (str or None): Model version identifier.
            - **tags** (list of DatasetTag or None): A list of tags related to the dataset.
            - **schema** (Schema): The schema of the dataset.  # noqa: E501
        """
        return self.api.create_dataset(dataset_create, **kwargs)

    @raise_exception
    def update(self, dataset_id, dataset_update: DatasetUpdate, **kwargs):
        """
        Update an existing Dataset

        - **payload** (DatasetUpdate): Required. The payload that includes:
            - **name** (str or None): Updated name of the dataset.
            - **description** (str or None): A revised description about the dataset.
            - **id** (str or None): Unique identifier of the dataset.
            - **model_version_id** (str or None): Updated model version identifier.
            - **created_by** (str or None): Identifier of the user who updated the dataset.
            - **tags** (list of str or None): A list of updated tags related to the dataset.
            - **schema** (SchemaUpdate or None): The updated schema of the dataset.
        """

        return self.api.update_dataset(dataset_id, dataset_update, **kwargs)

    def delete(self, dataset_id, **kwargs):
        """
        Delete a specific Dataset

        - **dataset_id** (str): Required, ID of the dataset to be deleted.
        """
        return self.api.delete_dataset(dataset_id, **kwargs)

    @raise_exception
    def get_by_id(self, dataset_id, **kwargs):
        """
        Fetch a specific Dataset

        - **dataset_id** (str): Required, ID of the dataset to be fetched.
        """

        return self.api.get_dataset(dataset_id, **kwargs)

    @raise_exception
    def get(self, **query_params):
        """
        Retrieve all Datasets based on provided filters

        - **name** (str or None): Optional, Name of the dataset based on which records to be fetched.
        - **description** (str or None): Optional, Description of the dataset based on which records to be fetched.
        - **id** (str or None): Optional, Unique identifier of the dataset based on which records to be fetched.
        - **model_version_id** (str or None): Optional, Model version identifier based on which datasets to be fetched.
        - **created_by** (str or None): Optional, Identifier of the user who created the datasets based on which datasets to be fetched.
        """

        return self.api.get_datasets(**query_params)

    @raise_exception
    def search(self, id_or_name_prefix: str, **kwargs):
        """
        Search for Datasets that match the provided prefix for id or name

        - **prefix** (str): Required, Dataset id/name prefix.
        """

        return self.api.search_datasets(id_or_name_prefix, **kwargs)
