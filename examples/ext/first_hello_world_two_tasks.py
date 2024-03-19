import asyncio

from dbgpt.core.awel import DAG, MapOperator, InputOperator, SimpleCallDataInputSource

with DAG("awel_hello_world") as dag:
    input_task = InputOperator(
        input_source=SimpleCallDataInputSource()
    )
    print("输入参数：", input_task)
    task = MapOperator(map_function=lambda x: print(f"Hello, {x}!"))
    input_task >> task

asyncio.run(task.call(call_data="world"))
