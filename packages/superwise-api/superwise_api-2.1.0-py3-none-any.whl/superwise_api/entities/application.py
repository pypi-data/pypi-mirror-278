from superwise_api.client import ApplicationsApi
from superwise_api.errors import raise_exception
from superwise_api.models.application.schemas import ApplicationConfigPayload
from superwise_api.models.application.schemas import AskRequestPayload
from superwise_api.models.application.schemas import ModelLLM


class Application:
    """
    Method | HTTP request | Description
    ------------- | ------------- | -------------
    **ask** | **POST** /v1/application-playground/ask | Ask
    **create_application** | **POST** /v1/applications | Create Application
    """

    def __init__(self, client):
        self.api = ApplicationsApi(client)

    @raise_exception
    def create(self, application_config_payload: ApplicationConfigPayload, **kwargs):
        """
        Create a new application.

        """
        return self.api.create_application(application_config_payload, **kwargs)

    @raise_exception
    def ask(self, ask_request_payload: AskRequestPayload, **kwargs):
        """
        Ask the application a question.

        Parameters:

        - **payload**: Instance of AskRequestPayload model.
            - **input**: Input to the application.
            - **config**: Configuration for the application is an ApplicationCreate model.
                - **name**: Name of the application.
                - **model_id**: UUID of the model.
                - **prompt**: Prompt for the application.
            - **chat_history**: Chat history for the application is a List[ChatHistoryEntry].
                - **role**: Role of the chat history entry. (HUMAN or AI)
                - **message**: Message of the chat history entry.
        """
        return self.api.ask_application(ask_request_payload, **kwargs)

    @raise_exception
    def get_applications(self, **query_params):
        """
        Get all applications. Filter if provided with name, created_by, or prompt.

        """
        return self.api.get_applications(**query_params)

    @raise_exception
    def get_application_by_id(self, application_id: str, **kwargs):
        """
        Get an application by its id.

        Parameters:

        - **application_id**: UUID of the application.
        """
        return self.api.get_application_by_id(application_id, **kwargs)

    @raise_exception
    def put(self, application_id: str, application_config_payload: ApplicationConfigPayload, **kwargs):
        """
        Update an application.

        """
        return self.api.put_application(application_id, application_config_payload, **kwargs)

    @raise_exception
    def delete(self, application_id: str, **kwargs):
        """
        Delete an application.

        Parameters:

        - **application_id**: UUID of the application.
        """
        return self.api.delete_application(application_id, **kwargs)

    @raise_exception
    def test_model_connection(self, model: ModelLLM, **kwargs):
        """
        Test the connection to the model.
        """
        return self.api.test_model_connection(model, **kwargs)
