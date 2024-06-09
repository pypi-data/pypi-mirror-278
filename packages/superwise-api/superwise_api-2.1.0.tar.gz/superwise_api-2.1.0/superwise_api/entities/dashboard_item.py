from superwise_api.client import DashboardItemCreate
from superwise_api.client import DashboardItemsApi
from superwise_api.errors import raise_exception


# from superwise_api.client import DashboardItemUpdate


class DashboardItem:
    """
        Method | HTTP request | Description
    ------------- | ------------- | -------------
    **create** | **POST** /v1/dashboard_items | Create dashboard item
    **delete** | **DELETE** /v1/dashboard_items/{dashboard_item_id} | Delete dashboard item
    **get_by_id** | **GET** /v1/dashboard_items/{dashboard_item_id} | Get dashboard item
    **get** | **GET** /v1/dashboard_items | Get dashboards items
    **update** | **PATCH** /v1/dashboard_items/{dashboard_item_id} | Update dashboard item
    """

    def __init__(self, client):
        self.api = DashboardItemsApi(client)

    @raise_exception
    def create(self, dashboard_item_create: DashboardItemCreate, **kwargs):
        """
        Create a new dashboard item

        - **payload** (DashboardCreate): Required. The payload that includes:
            - **name** (str): Name of the dashboard item
            - **dashboard_id** (UUID): dashboard id to which the dashboard item belongs
            - **query_type** (superwise_api.client.models.QueryType): Query type of the dashboard item
            - **visualization_type** (superwise_api.client.models.VisualizationType): TABLE | BARPLOT | LINECHART,
            - **datasource** (superwise_api.client.models.Datasource): Datasource of the dashboard item,
            - **query** (dict): Query of the dashboard item,
            - **item_metadata** (dict): Metadata of the dashboard item,
        """
        return self.api.create_dashboard_item(dashboard_item_create, **kwargs)

    # @raise_exception
    # def update(self, dashboard_id, dashboard_item_update: DashboardItemUpdate, **kwargs):
    #     """
    #     Update an existing dashboard
    #
    #     - **payload** (dashboardUpdate): Required. The payload that includes:
    #         - **name** (str or None): Updated name of the dashboard.
    #         - **positions** (dict or None): Update widgets positions of the dashboard. { UUID, WidgetMeta }
    #     """
    #     return self.api.update_dashboard(dashboard_id, dashboard_item_update)

    # @raise_exception
    # def delete(self, dashboard_item_id, **kwargs):
    #     """
    #     Delete a specific dashboard
    #
    #     - **dashboard_id** (str): Required, ID of the dashboard to be deleted.
    #     """
    #     return self.api.delete_dashboard_item(dashboard_item_id)

    @raise_exception
    def get_by_id(self, dashboard_id, **kwargs):
        """
        Fetch a specific dashboard

        - **dashboard_id** (str): Required, ID of the dashboard to be fetched.
        """

        return self.api.get_dashboard_item(dashboard_id, **kwargs)

    @raise_exception
    def get(self, **query_params):
        """
        Retrieve all dashboards based on provided filters

        - **name** (str or None): Optional, Name of the dashboard based on which records to be fetched.
        - **dashboard_id** (str or None): Optional, dashboard id.
        """

        return self.api.get_dashboards_items(**query_params)
