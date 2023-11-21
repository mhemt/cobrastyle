import time
from dataclasses import dataclass

from cobrastyle.typing import Event


@dataclass
class ClientContext:
    installation_id: str
    app_title: str
    app_version_name: str
    app_version_code: str
    app_package_name: str
    custom: dict
    env: dict


@dataclass
class CognitoIdentity:
    cognito_identity_id: str
    cognito_identity_pool_id: str


@dataclass
class Invocation:
    event: Event
    aws_request_id: str
    runtime_deadline: int
    invoked_function_arn: str
    trace_id: str | None = None
    client_context: ClientContext | None = None
    cognito_identity: CognitoIdentity | None = None


@dataclass
class Context:
    """Provide information about the invocation, function, and execution environment."""

    function_name: str
    function_version: str
    invoked_function_arn: str
    memory_limit_in_mb: int
    aws_request_id: str
    log_group_name: str
    log_stream_name: str
    _runtime_deadline: int
    client_context: ClientContext | None = None
    identity: CognitoIdentity | None = None

    def get_remaining_time(self) -> int:
        """Return the remaining time (in milliseconds) before Lambda times out."""

        return int(self._runtime_deadline - time.time() * 1000)
