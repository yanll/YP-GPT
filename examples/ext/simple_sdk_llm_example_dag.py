import os

from dbgpt.core import BaseOutputParser
from dbgpt.core.awel import DAG
from dbgpt.core.operators import (
    PromptBuilderOperator,
    RequestBuilderOperator,
)
from dbgpt.model.operators import LLMOperator
from dbgpt.model.proxy import OpenAILLMClient

with DAG("simple_sdk_llm_example_dag") as dag:
    prompt_task = PromptBuilderOperator(
        "Write a SQL of {dialect} to query all data of {table_name}."
    )
    model_pre_handle_task = RequestBuilderOperator(model="gpt-3.5-turbo")
    llm_task = LLMOperator(OpenAILLMClient())
    out_parse_task = BaseOutputParser()
    prompt_task >> model_pre_handle_task >> llm_task >> out_parse_task

os.environ['OPENAI_API_KEY'] = ''
os.environ['OPENAI_API_BASE'] = ''

print('开始运行...')