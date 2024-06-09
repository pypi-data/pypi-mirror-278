from superwise_api.client import PoliciesApi
from superwise_api.client import PolicyCreate
from superwise_api.client import PolicyUpdate
from superwise_api.errors import raise_exception


class Policy:
    """
        Method | HTTP request | Description
    ------------- | ------------- | -------------
    **create**| **POST** /v1/policies | Create Policy
    **delete**| **DELETE** /v1/policies/{policy_id} | Delete Policy
    **get_by_id**| **GET** /v1/policies/{policy_id} | Get Policy
    **get** | **GET** /v1/policies | Get Policies
    **update**| **PATCH** /v1/policies/{policy_id} | Update Policy
    **trigger** | **POST** /v1/policies/{policy_id}/trigger | Trigger Policy

    """

    def __init__(self, client):
        self.api = PoliciesApi(client)

    @raise_exception
    def create(self, policy_create: PolicyCreate, **kwargs):
        """
        Creates a new Policy

        - **payload** (PolicySchema): Required. The policy data to be created:
            - **name** (str): A descriptive name for this policy.
            - **query** (Query): Cube.js query.
            - **cron_expression** (str): Cron expression for policy evaluation.
            - **condition_above_value** (float or None): Condition above value.
            - **condition_below_value** (float or None): Condition below value.
            - **destination_ids** (list of UUID): List of communication channels to get notified through.
            - **alert_on_status** (AlertOnStatusDirection): Trigger policy action if the value is above/below.
            - **alert_on_policy_level** (bool): Trigger policy action on a single group/entire groups.
            - **dataset_id** (str): The dataset this policy is monitoring.
            - **time_range_field** (str): Time field to scan.
            - **time_range_unit** (TimeRangeUnit): Time unit to scan.
            - **time_range_value** (int): Time value to scan.
        """
        return self.api.create_policy(policy_create, **kwargs)

    @raise_exception
    def update(self, policy_id, policy_update: PolicyUpdate, **kwargs):
        """
        Update policy by ID.

        - **payload** (PolicyUpdate): Required. The updated policy information with:
            - **name** (str or None): The updated name of the policy.
            - **query** (Query or None): The updated Cube.js query for the policy.
            - **cron_expression** (str or None): The updated cron expression for the policy evaluation.
            - **condition_above_value** (float or None): The updated condition above value.
            - **condition_below_value** (float or None): The updated condition below value.
            - **destination_ids** (list of UUID or None): The updated list of communication channels to get notified through.
            - **alert_on_status** (AlertOnStatusDirection or None): The updated trigger policy action if the value is above/below.
            - **alert_on_policy_level** (bool or None): The updated trigger policy action on a single group/entire groups.
            - **dataset_id** (str or None): The updated dataset this policy is monitoring.
            - **time_range_field** (str or None): The updated time field to scan.
            - **time_range_unit** (TimeRangeUnit or None): The updated time unit to scan.
            - **time_range_value** (int or None): The updated time value to scan.
        - **policy_id** (UUID): Required. The ID of the policy to be updated.
        """
        return self.api.update_policy(policy_id, policy_update, **kwargs)

    @raise_exception
    def delete(self, policy_id, **kwargs):
        """
        Delete a specific Policy

        - **policy_id**: The ID of the policy to be deleted.
        """
        return self.api.delete_policy(policy_id, **kwargs)

    @raise_exception
    def get_by_id(self, policy_id, **kwargs):
        """
        Get policy by ID

        - policy_id (UUID): The ID of the policy.
        """
        return self.api.get_policy(policy_id, **kwargs)

    @raise_exception
    def get(self, **query_params):
        """
        Retrieve all Policies based on provided filters

        - **name** (str or None): Optional. The name of the policy to filter by.
        - **status** (PolicyStatus or None): Optional. The status of the policy to filter by.
        - **created_by** (str or None): Optional. The creator of the policy to filter by.
        - **dataset_id** (str or None): Optional. The ID of the dataset associated with the policy to filter by.
        """

        return self.api.get_policies(**query_params)

    @raise_exception
    def trigger(self, policy_id, **kwargs):
        """
        Trigger a source.

        - **policy_id**: UUID of the policy
        """
        return self.api.trigger_policy(policy_id, **kwargs)
