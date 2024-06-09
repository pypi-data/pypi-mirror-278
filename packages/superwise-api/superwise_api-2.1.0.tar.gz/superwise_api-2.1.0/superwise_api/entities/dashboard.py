from superwise_api.client import DashboardCreate
from superwise_api.client import DashboardsApi
from superwise_api.client import DashboardUpdate
from superwise_api.errors import raise_exception


class Dashboard:
    """
        Method | HTTP request | Description
    ------------- | ------------- | -------------
    **create** | **POST** /v1/dashboards | Create dashboard
    **delete** | **DELETE** /v1/dashboards/{dashboard_id} | Delete dashboard
    **get_by_id** | **GET** /v1/dashboards/{dashboard_id} | Get dashboard
    **get** | **GET** /v1/dashboards | Get dashboards
    **update** | **PATCH** /v1/dashboards/{dashboard_id} | Update dashboard

    """

    @raise_exception
    def __init__(self, client):
        self.api = DashboardsApi(client)

    @raise_exception
    def create(self, dashboard_create: DashboardCreate, **kwargs):
        """
        Create a new dashboard

        - **payload** (DashboardCreate): Required. The payload that includes:
            - **name** (str): Name of the dashboard, min_length=1, max_length=100.
        """
        return self.api.create_dashboard(dashboard_create, **kwargs)

    @raise_exception
    def update(self, dashboard_id, dashboard_update: DashboardUpdate, **kwargs):
        """
        Update an existing dashboard

        - **payload** (dashboardUpdate): Required. The payload that includes:
            - **name** (str or None): Updated name of the dashboard.
            - **positions** (dict or None): Update widgets positions of the dashboard. { WidgetID: UUID, WidgetMeta }
        """

        return self.api.update_dashboard(dashboard_id, dashboard_update, **kwargs)

    @raise_exception
    def delete(self, dashboard_id, **kwargs):
        """
        Delete a specific dashboard

        - **dashboard_id** (str): Required, ID of the dashboard to be deleted.
        """
        return self.api.delete_dashboard(dashboard_id, **kwargs)

    @raise_exception
    def get_by_id(self, dashboard_id, **kwargs):
        """
        Fetch a specific dashboard

        - **dashboard_id** (str): Required, ID of the dashboard to be fetched.
        """

        return self.api.get_dashboard(dashboard_id, **kwargs)

    @raise_exception
    def get(self, **query_params):
        """
        Retrieve all dashboards based on provided filters

        - **name** (str or None): Optional, Name of the dashboard based on which records to be fetched.
        - **description** (str or None): Optional, Description of the dashboard based on which records to be fetched.
        - **id** (str or None): Optional, Unique identifier of the dashboard based on which records to be fetched.
        - **model_version_id** (str or None): Optional, Model version identifier based on which dashboards to be fetched.
        - **created_by** (str or None): Optional, Identifier of the user who created the dashboards based on which dashboards to be fetched.
        """

        return self.api.get_dashboards(**query_params)
