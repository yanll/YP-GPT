from typing import Dict

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_project_api_wrapper


def call_lark_api(event: Dict):
    operator = event['operator']
    action = event['action']
    action_value = action['value']
    form_value = action['form_value']
    open_id = operator['open_id']
    union_id = operator['union_id']
    # open_id or union_id
    card_name = action_value['card_name']
    result = {}
    # 需求收集表单
    if (card_name == "requirement_collect"):
        result = create_requirement_for_lark_project(
            union_id=union_id, form_value=form_value
        )
    elif card_name == "daily_report_collect":
        #
        pass
    print("lark_openapi_call_result:", result)
    return result


def create_requirement_for_lark_project(union_id: str, form_value: Dict):
    return lark_project_api_wrapper.create_requirement_for_lark_project(
        union_id=union_id,
        name=form_value['requirement_content'],
        priority_value=form_value['emergency_level'],
        expected_time=form_value['expected_completion_date']
    )
