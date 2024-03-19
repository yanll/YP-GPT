from dbgpt._private.pydantic import BaseModel, Field
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator


class TriggerReqBody(BaseModel):
    name: str = Field(..., description="User name")
    age: int = Field(18, description="User age")


class RequestHandleOperator(MapOperator[TriggerReqBody, str]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def map(self, input_value: TriggerReqBody) -> str:
        print(f"Receive input value: {input_value}")
        return f"Hello, {input_value.name}, your age is {input_value.age}"


class RequestHandleOperator(MapOperator[TriggerReqBody, str]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def map(self, input_value: TriggerReqBody) -> str:
        print(f"Receive input value: {input_value}")
        return f"Hello, {input_value.name}, your age is {input_value.age}"


with DAG("simple_dag_example") as dag:
    trigger = HttpTrigger("/examples/hello", request_body=TriggerReqBody)
    map_node = RequestHandleOperator()
    trigger >> map_node





if __name__ == "__main__":
    if dag.leaf_nodes[0].dev_mode:
        # Development mode, you can run the dag locally for debugging.
        from dbgpt.core.awel import setup_dev_environment

        setup_dev_environment([dag], port=5555)
    else:
        # Production mode, DB-GPT will automatically load and execute the current file after startup.
        pass