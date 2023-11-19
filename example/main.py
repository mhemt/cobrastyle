from cobrastyle.clients import LambdaClient
from cobrastyle.runtimes import LambdaRuntime


def get_runtime() -> LambdaRuntime:
    return LambdaRuntime(lambda_client=LambdaClient())


def some_handler(event, context):
    print(event)
    print(context)


def main():
    runtime = get_runtime()
    runtime.run(some_handler)


if __name__ == '__main__':
    main()
