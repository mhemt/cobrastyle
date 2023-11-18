import traceback
from typing import Any, Callable

from constants import (
    AWS_LAMBDA_FUNCTION_MEMORY_SIZE,
    AWS_LAMBDA_FUNCTION_NAME,
    AWS_LAMBDA_FUNCTION_VERSION,
    AWS_LAMBDA_LOG_GROUP_NAME,
    AWS_LAMBDA_LOG_STREAM_NAME,
)
from runtimes.abstracts import AbstractLambdaClient
from runtimes.models import Context, Invocation


def get_context(invocation: Invocation, aws_request_id: str) -> Context:
    return Context(
        function_name=AWS_LAMBDA_FUNCTION_NAME,
        function_version=AWS_LAMBDA_FUNCTION_VERSION,
        invoked_function_arn=invocation.invoked_function_arn,
        memory_limit_in_mb=AWS_LAMBDA_FUNCTION_MEMORY_SIZE,
        aws_request_id=aws_request_id,
        log_group_name=AWS_LAMBDA_LOG_GROUP_NAME,
        log_stream_name=AWS_LAMBDA_LOG_STREAM_NAME,
        client_context=invocation.client_context,
        identity=invocation.cognito_identity,
        runtime_deadline=invocation.runtime_deadline,
    )


class LambdaRuntime:
    def __init__(self, lambda_client: AbstractLambdaClient) -> None:
        self.client = lambda_client

    def run(self, lambda_handler: Callable[[dict[str, Any], Context], Any]) -> None:
        while True:
            invocation = self.client.get_next_invocation()

            aws_request_id = invocation.aws_request_id
            context = get_context(invocation, aws_request_id)

            try:
                lambda_handler(invocation.event, context)
            except Exception:  # TODO: is it possible to get rid of the broad exception?
                traceback.print_exc()
                self.client.post_invocation_error(aws_request_id)
            else:
                self.client.post_invocation_response(aws_request_id)
