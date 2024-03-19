import asyncio
from typing import AsyncIterator
from dbgpt.core.awel import DAG, StreamifyAbsOperator, TransformStreamAbsOperator


class NumberProducerOperator(StreamifyAbsOperator[int, int]):
    async def streamify(self, n: int) -> AsyncIterator[int]:
        for i in range(n):
            yield i


class NumberDoubleOperator(TransformStreamAbsOperator[int, int]):
    async def transform_stream(self, it: AsyncIterator) -> AsyncIterator[int]:
        async for i in it:
            # Double the number
            yield i * 2


with DAG("numbers_dag") as dag:
    task = NumberProducerOperator()
    double_task = NumberDoubleOperator()
    task >> double_task


async def helper_call_fn(t, n: int):
    # Call the streaming operator by `call_stream` method
    async for i in await t.call_stream(call_data=n):
        print(i)


asyncio.run(helper_call_fn(double_task, 10))
