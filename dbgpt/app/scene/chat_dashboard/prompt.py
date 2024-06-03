import json

from dbgpt._private.config import Config
from dbgpt.app.scene import AppScenePromptTemplateAdapter, ChatScene
from dbgpt.app.scene.chat_dashboard.out_parser import ChatDashboardOutputParser
from dbgpt.core import ChatPromptTemplate, HumanPromptTemplate, SystemPromptTemplate

CFG = Config()

PROMPT_SCENE_DEFINE = "您是一名数据分析专家，请提供专业的数据分析解决方案。"

_DEFAULT_TEMPLATE = """
根据以下表结构定义：
{table_info}
提供专业的数据分析以支持用户目标：
{input}

根据用户目标提供至少4个且不超过8个分析维度。
分析输出的数据不能超过4列，并且在SQL的where条件中不要使用pay_status等列进行数据筛选。
根据分析数据的特点，一定要从下列提供的图表类型中选择最合适的一种进行数据展示，图表类型：
{supported_chat_type}

注意分析结果的输出内容长度，不超过4000个tokens。

给出正确的{dialect}分析SQL

不要使用未提供的值，例如'paid'
所有查询的值必须有别名，例如select count(*) as count from table
如果表结构定义使用了{dialect}的关键字作为字段名，需要使用转义字符，例如select count from table
写SQL时，根据图表类型从左到右排序字段，从x开始到y。
仔细检查SQL的正确性，SQL必须正确，显示方法和简要分析思路总结，并以以下json格式响应：
{response}
重要的是：请确保只返回json字符串，不要添加任何其他内容（以便程序直接处理），并且json可以通过Python的json.loads解析。
请使用与“用户”相同的语言。
"""

RESPONSE_FORMAT = [
    {
        "thoughts": "当前数据分析的思维和价值",
        "showcase": "图表类型",
        "sql": "数据分析 SQL",
        "title": "数据分析标题",
        # "columns_sort": "Sort the fields based on the type of chart to be displayed, from left to right, and from x to y."
    }
]

PROMPT_NEED_STREAM_OUT = False

prompt = ChatPromptTemplate(
    messages=[
        SystemPromptTemplate.from_template(
            PROMPT_SCENE_DEFINE + _DEFAULT_TEMPLATE,
            response_format=json.dumps(RESPONSE_FORMAT, indent=4),
        ),
        HumanPromptTemplate.from_template("{input}"),
    ]
)

prompt_adapter = AppScenePromptTemplateAdapter(
    prompt=prompt,
    template_scene=ChatScene.ChatDashboard.value(),
    stream_out=PROMPT_NEED_STREAM_OUT,
    output_parser=ChatDashboardOutputParser(is_stream_out=PROMPT_NEED_STREAM_OUT),
    need_historical_messages=False,
)
CFG.prompt_template_registry.register(prompt_adapter, is_default=True)
