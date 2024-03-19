import asyncio
from dbgpt.core.awel import DAG, MapOperator


class HelloWorldOperator(MapOperator[str, None]):
    async def map(self, x: str) -> None:
        print(f"Hello, {x}!")


with DAG("awel_hello_world") as dag:
    task = HelloWorldOperator()

asyncio.run(task.call(call_data="world"))