from functools import wraps

from superwise_api.client import ApiAttributeError
from superwise_api.client import ApiException
from superwise_api.client import ApiKeyError
from superwise_api.client import ApiTypeError
from superwise_api.client import ApiValueError
from superwise_api.client.exceptions import BadRequestException
from superwise_api.client.exceptions import ForbiddenException
from superwise_api.client.exceptions import NotFoundException
from superwise_api.client.exceptions import ServiceException


class SuperwiseApiException(Exception):
    """
    Base class for exceptions in the Superwise API.
    """

    def __init__(self, original_exception, message="Superwise API Error"):
        self.original_exception = original_exception
        self.message = message
        super().__init__(str(original_exception))

    def __str__(self):
        return f"{self.message}: {self.original_exception}"


def raise_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApiException as e:
            raise SuperwiseApiException(original_exception=e, message=e.body)
        except (ApiTypeError, ApiValueError, ApiAttributeError, ApiKeyError) as e:
            raise e
        except Exception as e:
            # Catch any other exceptions that were not anticipated
            raise SuperwiseApiException(e, message="A general error occurred - We are looking into it")

    return wrapper
