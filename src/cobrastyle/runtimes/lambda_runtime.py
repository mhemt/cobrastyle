import time
import traceback
from threading import Thread
from typing import Any, Callable

from cobrastyle.constants import (
    AWS_LAMBDA_FUNCTION_MEMORY_SIZE,
    AWS_LAMBDA_FUNCTION_NAME,
    AWS_LAMBDA_FUNCTION_VERSION,
    AWS_LAMBDA_LOG_GROUP_NAME,
    AWS_LAMBDA_LOG_STREAM_NAME,
)
from cobrastyle.runtimes.abstracts import AbstractLambdaClient
from cobrastyle.runtimes.models import Context, Invocation


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


def print_ping():
    while True:
        print('ping')
        time.sleep(0.1)


class LambdaRuntime:
    def __init__(self, lambda_client: AbstractLambdaClient) -> None:
        self.client = lambda_client

    def run(self, lambda_handler: Callable[[dict[str, Any], Context], Any]) -> None:
        # Catch all runtime exceptions and let AWS Lambda API know about them
        try:
            self._try_run(lambda_handler)
        except Exception:
            self.client.post_init_error()

    def _try_run(self, lambda_handler: Callable[[dict[str, Any], Context], Any]) -> None:
        print('START PING THREAD')
        thread = Thread(target=print_ping)
        thread.start()

        while True:
            print('START WHILE CYCLE')
            invocation = self.client.get_next_invocation()
            print('INVOCATION RECEIVED')
            aws_request_id = invocation.aws_request_id
            context = get_context(invocation, aws_request_id)

            # Catch all handler exceptions and let AWS Lambda API know about them
            try:
                print('START EVENT HANDLING')
                result = lambda_handler(invocation.event, context)
            except Exception:
                traceback.print_exc()
                self.client.post_invocation_error(aws_request_id)
            else:
                self.client.post_invocation_response(aws_request_id, result)


class AsyncLambdaRuntime:
    def __init__(self, lambda_client: AbstractLambdaClient) -> None:
        self.client = lambda_client

    async def run(self, lambda_handler: Callable[[dict[str, Any], Context], Any]) -> None:
        # Catch all runtime exceptions and let AWS Lambda API know about them
        try:
            await self._try_run(lambda_handler)
        except Exception:
            await self.client.post_init_error()

    async def _try_run(self, lambda_handler: Callable[[dict[str, Any], Context], Any]) -> None:
        while True:
            invocation = await self.client.get_next_invocation()

            aws_request_id = invocation.aws_request_id
            context = get_context(invocation, aws_request_id)

            # Catch all handler exceptions and let AWS Lambda API know about them
            try:
                result = await lambda_handler(invocation.event, context)
            except Exception:
                traceback.print_exc()
                await self.client.post_invocation_error(aws_request_id)
            else:
                await self.client.post_invocation_response(aws_request_id, result)
