from superwise_api.client import DestinationCreateBase
from superwise_api.client import DestinationsApi
from superwise_api.client import DestinationUpdateBase
from superwise_api.errors import raise_exception


class Destination:
    """
        Method | HTTP request | Description
    ------------- | ------------- | -------------
    **create**| **POST** /v1/destinations | Create Destination
    **delete**| **DELETE** /v1/destinations/{destination_id} | Delete Destination
    **get_by_id**| **GET** /v1/destinations/{destination_id} | Get Destination
    **get**| **GET** /v1/destinations | Get Sources
    **update**| **PATCH** /v1/destinations/{destination_id} | Update Destination

    """

    def __init__(self, client):
        self.api = DestinationsApi(client)

    @raise_exception
    def create(self, destination_create: DestinationCreateBase, **kwargs):
        """
        Create a new destination

        - **base_destination_create** (DestinationCreateBase): Required. The payload that includes:
            - **name** (str): Name of the new destination.
            - **integration_id** (UUID): Unique identifier of the integration to which the destination would be created.
            - **params** (dict): Additional parameters for the creation of the destination.
        """
        return self.api.create_destination(destination_create, **kwargs)

    @raise_exception
    def update(self, destination_id, destination_update: DestinationUpdateBase, **kwargs):
        """
        Update a specific destination by ID

        - **base_destination_update** (DestinationUpdateBase): The payload containing the update data for the destination, which includes:
            - **name** (str): The updated name of the destination.
            - **params** (dict): A dictionary containing key-value pairs for parameters to be updated.
        """
        return self.api.update_destination(destination_id, destination_update, **kwargs)

    @raise_exception
    def delete(self, destination_id, **kwargs):
        """
        Delete a specific destination by ID

        - **destination_id** (UUID): The unique identifier of the destination.
        """
        return self.api.delete_destination(destination_id, **kwargs)

    @raise_exception
    def get_by_id(self, destination_id):
        """
        Get a specific destination by ID

        - **destination_id** (UUID): The unique identifier of the destination.
        """
        return self.api.get_destination(destination_id, **kwargs)

    @raise_exception
    def get(self, **query_params):
        """
        Get all available destinations based on the provided filters

        - **destination_id** (List[UUID]): Optional filter by destination IDs.
        - **integration_id** (List[UUID]): Optional filter by related integration IDs.
        - **name** (List[str]): Optional filter by destination names.
        - **created_by** (List[str]): Optional filter by creation user IDs.
        """

        return self.api.get_destinations(**query_params)
