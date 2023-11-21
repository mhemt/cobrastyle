from abc import ABC, abstractmethod
from http.client import HTTPResponse
from typing import Any, Callable

from cobrastyle.runtimes.models import Context, Invocation
from cobrastyle.typing import Event


class AbstractLambdaClient(ABC):
    """
    A client to work with Lambda runtime API.
    https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html
    """

    @abstractmethod
    def get_next_invocation(self) -> Invocation:
        """
        Request an invocation event.
        https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html#runtimes-api-next

        Return:
            An Invocation object.
        """
        pass

    @abstractmethod
    def post_invocation_response(self, aws_request_id: str, result: Any) -> HTTPResponse:
        """
        Send an invocation response to Lambda.
        https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html#runtimes-api-response

        Args:
            aws_request_id: the identifier of the invocation request.
            result: a lambda handler return value that can be JSON-serialized.
        Return:
            A HTTPResponse object.
        """
        pass

    @abstractmethod
    def post_invocation_error(self, aws_request_id: str) -> HTTPResponse:
        """
        Report an invocation error to Lambda.
        https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html#runtimes-api-initerror

        Args:
            aws_request_id: the identifier of the invocation request.
        Return:
            A HTTPResponse object.
        """
        pass

    @abstractmethod
    def post_init_error(self) -> HTTPResponse:
        """
        Report an initialization error to Lambda.
        https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html#runtimes-api-invokeerror

        Return:
            A HTTPResponse object.
        """
        pass


class AbstractLambdaRuntime(ABC):
    """A runtime that manages a Lambda client and a Lambda handler."""

    @abstractmethod
    def run(self, lambda_handler: Callable[[Event, Context], Any]) -> None:
        """
        Receive an event, execute a Lambda handler, and report an execution result.

        Args:
            lambda_handler: a handler function to execute.
        """
        pass
