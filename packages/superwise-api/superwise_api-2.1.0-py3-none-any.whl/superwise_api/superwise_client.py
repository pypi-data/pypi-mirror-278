from typing import Optional

import requests

from superwise_api import models
from superwise_api.client.api_client import ApiClient
from superwise_api.client.exceptions import UnauthorizedException
from superwise_api.config import Settings
from superwise_api.entities.application import Application
from superwise_api.entities.dashboard import Dashboard
from superwise_api.entities.dashboard_item import DashboardItem
from superwise_api.entities.dataset import Dataset
from superwise_api.entities.dataset_source import DatasetSource
from superwise_api.entities.destination import Destination
from superwise_api.entities.integration import Integration
from superwise_api.entities.policy import Policy
from superwise_api.entities.source import Source


class SuperwiseClient(ApiClient):
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        auth_host: Optional[str] = None,
        api_host: Optional[str] = None,
        use_hosted_auth: Optional[bool] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        params_without_none_values = {k: v for k, v in locals().items() if v is not None}
        self.settings = Settings(
            **params_without_none_values,
        )
        self.configuration.host = self.settings.api_host
        self.configuration.access_token = self._fetch_token(
            auth_url=self.settings.auth_url,
            client_id=self.settings.client_id,
            client_secret=self.settings.client_secret,
        )

    @property
    def dataset(self):
        """
        **Dataset** | [**create**](../docs/dataset/schemas/DatasetApi.md#create_dataset) | **POST** /v1/datasets | Create Dataset

        **Dataset** | [**delete**](../docs/dataset/schemas/DatasetApi.md#delete_dataset) | **DELETE** /v1/datasets/{dataset_id} | Delete Dataset

        **Dataset** | [**get_by_id**](../docs/dataset/schemas/DatasetApi.md#get_dataset) | **GET** /v1/datasets/{dataset_id} | Get Dataset

        **Dataset** | [**get**](../docs/dataset/schemas/DatasetApi.md#get_datasets) | **GET** /v1/datasets | Get Datasets

        **Dataset** | [**search_datasets**](../docs/dataset/schemas/DatasetApi.md#search_datasets) | **GET** /v1/datasets/search/{prefix} | Search Datasets

        **Dataset** | [**update**](../docs/dataset/schemas/DatasetApi.md#update_dataset) | **PATCH** /v1/datasets/{dataset_id} | Update Dataset
        """
        return Dataset(self)

    @property
    def policy(self):
        """
        **Policy** | [**create_policy**](../docs/policy/schemasPoliciesApi.md#create_policy) | **POST** /v1/policies | Create Policy

        **Policy** | [**delete_policy**](../docs/policy/schemasPoliciesApi.md#delete_policy) | **DELETE** /v1/policies/{policy_id} | Delete policy by ID

        **Policy** | [**get_policies**](../docs/policy/schemasPoliciesApi.md#get_policies) | **GET** /v1/policies | Get Policies

        **Policy** | [**get_policy**](../docs/policy/schemasPoliciesApi.md#get_policy) | **GET** /v1/policies/{policy_id} | Get Policy By Id

        **Policy** | [**trigger_policy**](../docs/policy/schemasPoliciesApi.md#trigger_policy) | **POST** /v1/policies/{policy_id}/trigger | Trigger policy by ID

        **Policy** | [**update_policy**](../docs/policy/schemasPoliciesApi.md#update_policy) | **PATCH** /v1/policies/{policy_id} | Update policy by ID
        """
        return Policy(self)

    @property
    def destination(self):
        """
        **Destination** | [**create_destination**](../docs/destination/schemasDestinationsApi.md#create_destination) | **POST** /v1/destinations | Create Destination

        **Destination** | [**delete_destination**](../docs/destination/schemasDestinationsApi.md#delete_destination) | **DELETE** /v1/destinations/{destination_id} | Delete Destination By Id

        **Destination** | [**get_destination**](../docs/destination/schemasDestinationsApi.md#get_destination) | **GET** /v1/destinations/{destination_id} | Get Destination By Id

        **Destination** | [**get_destinations**](../docs/destination/schemasDestinationsApi.md#get_destinations) | **GET** /v1/destinations | Get Destinations

        **Destination** | [**update_destination**](../docs/destination/schemasDestinationsApi.md#update_destination) | **PATCH** /v1/destinations/{destination_id} | Update Destination By Id
        """
        return Destination(self)

    @property
    def integration(self):
        """
        **Integration** | [**delete_integration**](../docs/integration/schemasIntegrationsApi.md#delete_integration) | **DELETE** /v1/integrations/{integration_id} | Delete Integration By Id

        **Integration** | [**get_integration**](../docs/integration/schemasIntegrationsApi.md#get_integration) | **GET** /v1/integrations/{integration_id} | Get Integration By Id

        **Integration** | [**get_integrations**](../docs/integration/schemasIntegrationsApi.md#get_integrations) | **GET** /v1/integrations | Get Integrations
        """
        return Integration(self)

    @property
    def source(self):
        """
        **Source** | [**create_source**](../docs/source/schemas/SourcesApi.md#create_source) | **POST** /v1/sources | Create Source

        **Source** | [**delete_source**](../docs/source/schemas/SourcesApi.md#delete_source) | **DELETE** /v1/sources/{source_id} | Delete Source

        **Source** | [**get_source**](../docs/source/schemas/SourcesApi.md#get_source) | **GET** /v1/sources/{source_id} | Get Source

        **Source** | [**get_sources**](../docs/source/schemas/SourcesApi.md#get_sources) | **GET** /v1/sources | Get Sources

        **Source** | [**update_source**](../docs/source/schemas/SourcesApi.md#update_source) | **PATCH** /v1/sources/{source_id} | Update Source
        """
        return Source(self)

    @property
    def dataset_source(self):
        """
        **DatasetSource** | [**create_dataset_source**](../docs/dataset_source/schemasDatasetSourcesApi.md#create_dataset_source) | **POST** /v1/dataset-sources | Create Dataset Source

        **DatasetSource** | [**delete_dataset_source**](../docs/dataset_source/schemasDatasetSourcesApi.md#delete_dataset_source) | **DELETE** /v1/dataset-sources/{dataset_source_id} | Delete Dataset Source

        **DatasetSource** | [**get_dataset_source**](../docs/dataset_source/schemasDatasetSourcesApi.md#get_dataset_source) | **GET** /v1/dataset-sources/{dataset_source_id} | Get Dataset Source

        **DatasetSource** | [**get_dataset_sources**](../docs/dataset_source/schemasDatasetSourcesApi.md#get_dataset_sources) | **GET** /v1/dataset-sources | Get Dataset Sources

        **DatasetSource** | [**update_dataset_source**](../docs/dataset_source/schemasDatasetSourcesApi.md#update_dataset_source) | **PATCH** /v1/dataset-sources/{dataset_source_id} | Update Dataset Source
        """
        return DatasetSource(self)

    @property
    def dashboard(self):
        """
        *DashboardsApi* | [**create_dashboard**](../docs/dashboard/schemas/DashboardsApi.md#create_dashboard) | **POST** /v1/dashboards | Create Dashboard

        *DashboardsApi* | [**delete_dashboard**](../docs/dashboard/schemas/DashboardsApi.md#delete_dashboard) | **DELETE** /v1/dashboards/{dashboard_id} | Delete dashboard by ID

        *DashboardsApi* | [**get_dashboard**](../docs/dashboard/schemas/DashboardsApi.md#get_dashboard) | **GET** /v1/dashboards/{dashboard_id} | Get Dashboard

        *DashboardsApi* | [**get_dashboards**](../docs/dashboard/schemas/DashboardsApi.md#get_dashboards) | **GET** /v1/dashboards | Get Dashboards

        *DashboardsApi* | [**update_dashboard**](../docs/dashboard/schemas/DashboardsApi.md#update_dashboard) | **PATCH** /v1/dashboards/{dashboard_id} | Update dashboard by ID
        """
        return Dashboard(self)

    @property
    def dashboard_item(self):
        """
        *DashboardItemsApi* | [**create_dashboard_item**](../docs/dashboard_item/schemas/DashboardItemsApi.md#create_dashboard_item) | **POST** /v1/dashboard-items | Create Dashboard Item

        *DashboardItemsApi* | [**get_dashboard_item**](../docs/dashboard_item/schemas/DashboardItemsApi.md#get_dashboard_item) | **GET** /v1/dashboard-items/{dashboard_item_id} | Get Dashboard

        *DashboardItemsApi* | [**get_dashboards_items**](../docs/dashboard_item/schemas/DashboardItemsApi.md#get_dashboards_items) | **GET** /v1/dashboard-items | Get Dashboards Items
        """
        return DashboardItem(self)

    @property
    def application(self):
        """
        *ApplicationsApi* | [**ask**](../docs/application/schemas/ApplicationsApi.md#ask) | **POST** /v1/application-playground/ask | Ask

        *ApplicationsApi* | [**create_application**](../docs/application/schemas/ApplicationsApi.md#create_application) | **POST** /v1/applications | Create Application
        """
        return Application(self)

    @staticmethod
    def _fetch_token(auth_url: str, client_id: str, client_secret: str) -> str:
        response = requests.post(
            auth_url,
            json={
                "clientId": client_id,
                "secret": client_secret,
            },
            headers={"accept": "application/json", "content-type": "application/json"},
        )
        response.raise_for_status()
        return response.json()["accessToken"]

    def call_api(self, *args, **kwargs):
        try:
            return super().call_api(*args, **kwargs)
        except UnauthorizedException:
            self.configuration.access_token = self._fetch_token(
                auth_url=self.settings.auth_url,
                client_id=self.settings.client_id,
                client_secret=self.settings.client_secret,
            )
            return super().call_api(*args, **kwargs)

    def _ApiClient__deserialize(self, data, klass):
        if klass in models.__all__:
            return getattr(models, klass).from_dict(data)

        return super()._ApiClient__deserialize(data, klass)

    def request(self, *args, **kwargs):
        response = super().request(*args, **kwargs)

        if response.status == 204 and not response.data:
            response.data = b"{}"

        return response
