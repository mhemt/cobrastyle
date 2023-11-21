from abc import ABC, abstractmethod
from http.client import HTTPResponse
from typing import Any

from cobrastyle.runtimes.models import Invocation


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

        Returns:
            An Invocation object.
        """
        pass

    @abstractmethod
    def post_invocation_response(self, aws_request_id: str, result: Any) -> HTTPResponse:
        """
        Send an invocation response to Lambda.
        https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html#runtimes-api-response

        Params:
            aws_request_id:
            result:
        Return:
            A HTTPResponse object.
        """
        pass

    @abstractmethod
    def post_invocation_error(self, aws_request_id: str) -> HTTPResponse:
        """
        Report an invocation error to Lambda.
        https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html#runtimes-api-initerror
        """
        pass

    @abstractmethod
    def post_init_error(self) -> HTTPResponse:
        """
        Report an initialization error to Lambda.
        https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html#runtimes-api-invokeerror
        """
        pass
