from cobrastyle.clients import LambdaClient
from cobrastyle.models import Context
from cobrastyle.runtimes import LambdaRuntime
from cobrastyle.typing import Event


def get_runtime() -> LambdaRuntime:
    return LambdaRuntime(lambda_client=LambdaClient())


def some_handler(event: Event, context: Context) -> None:
    print(event)
    print(context)


def main() -> None:
    runtime = get_runtime()
    runtime.run(some_handler)


if __name__ == '__main__':
    main()
