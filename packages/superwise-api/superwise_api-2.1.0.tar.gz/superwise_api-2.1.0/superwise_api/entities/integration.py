from superwise_api.client import IntegrationsApi
from superwise_api.errors import raise_exception


class Integration:
    """
        Method | HTTP request | Description
    ------------- | ------------- | -------------
    **delete**| **DELETE** /v1/integrations/{integration_id} | Delete Integration
    **get_by_id**| **GET** /v1/integrations/{integration_id} | Get Integration
    **get**| **GET** /v1/integrations | Get Sources

    """

    def __init__(self, client):
        self.api = IntegrationsApi(client)

    @raise_exception
    def delete(self, integration_id, **kwargs):
        """
        Delete a specific integration by ID

        - **integration_id** (UUID): The unique identifier of the integration.
        - **delete_destinations** (bool): Whether to delete destinations associated with the integration.
        """

        return self.api.delete_integration(integration_id, **kwargs)

    @raise_exception
    def get_by_id(self, integration_id, **kwargs):
        """
        Get a specific integration by ID

        - **integration_id** (UUID): The unique identifier of the integration.
        """
        return self.api.get_integration(integration_id, **kwargs)

    @raise_exception
    def get(self, **query_params):
        """
        Get all available integrations

        - **integration_type** (IntegrationType): Optional filter by integration type
        - **created_by** (str): Optional filter by user ID who created the integration.
        """
        return self.api.get_integrations(**query_params)
