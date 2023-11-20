import asyncio
from typing import Any

from cobrastyle.clients import AsyncLambdaClient
from cobrastyle.runtimes import AsyncLambdaRuntime
from cobrastyle.runtimes.models import Context


def get_runtime() -> AsyncLambdaRuntime:
    return AsyncLambdaRuntime(lambda_client=AsyncLambdaClient())


async def some_handler(event: dict[str, Any], context: Context) -> None:
    print(event)
    print(context)


async def main() -> None:
    runtime = get_runtime()
    await runtime.run(some_handler)


if __name__ == '__main__':
    asyncio.run(main())
