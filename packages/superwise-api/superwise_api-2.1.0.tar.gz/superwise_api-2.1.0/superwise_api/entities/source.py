from typing import Union

from superwise_api.client import SourcesApi
from superwise_api.errors import raise_exception
from superwise_api.models import SourceCreateAzure
from superwise_api.models import SourceCreateGCS
from superwise_api.models import SourceCreatePayload
from superwise_api.models import SourceCreateS3
from superwise_api.models import SourceUpdate
from superwise_api.models import SourceUpdateGCS
from superwise_api.models import SourceUpdateS3


class Source:
    """
        Method | HTTP request | Description
    ------------- | ------------- | -------------
    **create**| **POST** /v1/sources | Create Source
    **delete**| **DELETE** /v1/sources/{source_id} | Delete Source
    **get_by_id**| **GET** /v1/sources/{source_id} | Get Source
    **get**| **GET** /v1/sources | Get Sources
    **update**| **PATCH** /v1/sources/{source_id} | Update Source

    """

    def __init__(self, client):
        self.api = SourcesApi(client)

    @raise_exception
    def create(
        self, source_create: Union[SourceCreatePayload, SourceCreateGCS, SourceCreateAzure, SourceCreateS3], **kwargs
    ):
        """
            Create a new source.

        The SourceCreate model is defined by either the SourceCreateGCS, SourceCreateAzure or SourceCreateS3 classes, based on the source type.

        Parameters:

        - **payload**: Instance of SourceCreate model which can be any one of the following based on source type:
           - **SourceCreateGCS**
                - **type**: Literal, Source Type GCS.
                - **params**: SourceGCSParams object or None. Parameters for GCS source.
                - **credentials**: GCPCredentials object or None. Credentials for GCS source.
                - Validation is applied on the `credentials` field based on the hosting type.
           - **SourceCreateAzure**
                - **type**: Literal, Source type AZURE_BLOB_STORAGE.
                - **params**: SourceAzureParams object. Parameters for Azure source.
                - **credentials**: AzureCredentials object. Credentials for Azure source.
           - **SourceCreateS3**
                - **type**: Literal, Source type S3.
                - **params**: SourceS3Params object. Parameters for S3 source.
                - **credentials**: AWSCredentials object. Credentials for AWS source.
        """
        source_type = source_create.type
        if (
            isinstance(source_create, SourceCreateGCS)
            or isinstance(source_create, SourceCreateAzure)
            or isinstance(source_create, SourceCreateS3)
        ):
            source_create = SourceCreatePayload(source_create)
        else:
            raise ValueError(
                f"Invalid source type {source_type}, please use SourceCreateAzure or SourceCreateGCS or SourceCreateS3"
            )

        source = self.api.create_source(source_create, **kwargs)
        return source.actual_instance

    @raise_exception
    def update(self, source_id, source_update: Union[SourceUpdate, SourceUpdateGCS, SourceUpdateS3], **kwargs):
        """
        Update an existing source.

        The SourceUpdate Model is defined by the SourceUpdateGCS or SourceUpdateS3 class, based on the source type.

        Parameters:

        - **source_id**: UUID of the source to update.

        - **payload**: Instance of SourceUpdate model which can be any one of the following based on source type:
           - **SourceUpdateGCS**
                - **type**: Literal, Source Type GCS.
                - **params**: SourceGCSParams object or None. Parameters for GCS source.
                - **credentials**: GCPCredentials object or None. Credentials for GCS source.
           - **SourceUpdateS3**
                - **type**: Literal, Source type S3.
                - **params**: SourceS3Params object or None. Parameters for S3 source.
                - **credentials**: AWSCredentials object or None. Credentials for AWS source.
        """
        source_type = source_update.type
        if isinstance(source_update, SourceUpdateGCS) or isinstance(source_update, SourceUpdateS3):
            source_update = SourceUpdate(source_update)
        else:
            raise ValueError(
                f"Invalid source type {source_type}, please use SourceUpdateAzure or SourceUpdateGCS or SourceUpdateS3"
            )
        source = self.api.update_source(source_id, source_update, **kwargs)
        return source.actual_instance

    @raise_exception
    def delete(self, source_id, **kwargs):
        """
        Delete a specific source.

        - **source_id**: UUID of the source
        """
        return self.api.delete_source(source_id, **kwargs)

    @raise_exception
    def get_by_id(self, source_id, **kwargs):
        """
        Retrieve a Source based on the given source_id.

        - **source_id**: UUID of the source
        """
        source = self.api.get_source(source_id, **kwargs)
        return source.actual_instance

    @raise_exception
    def get(self, **query_params):
        """
        Retrieve all sources based on the provided filters.

        - **name**: Name of the source
        - **created_by**: Creator of the source
        - **created_at**: When the source was created
        - **updated_at**: When the source was last updated
        - **type**: Type of the source
        """
        return self.api.get_sources(**query_params)
