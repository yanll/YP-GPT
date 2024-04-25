from typing import Dict

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_api_wrapper
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_project_api_wrapper


def call(event: Dict):
    result = {}
    card_name = ""
    operator = event['operator']
    action = event['action']
    if "value" in action:
        action_value = action['value']
        card_name = action_value['card_name']
    if "form_value" not in action:
        print("表单内容为空，跳过执行：", event)
        return result
    form_value = action['form_value']
    open_id = operator['open_id']
    union_id = operator['union_id']
    # open_id or union_id
    # 需求收集表单
    if card_name == "requirement_collect":
        result = create_requirement_for_lark_project(
            union_id=union_id, form_value=form_value
        )
    elif card_name == "daily_report_collect":
        result = create_daily_report_for_crem(
            form_value=form_value
        )
    print("call_lark_api_result:", result)
    return result


def create_requirement_for_lark_project(union_id: str, form_value: Dict):
    return lark_project_api_wrapper.create_requirement_for_lark_project(
        project_key="ypgptapi",
        union_id=union_id,
        name=form_value['requirement_content'],
        priority_value=form_value['emergency_level'],
        expected_time=form_value['expected_completion_date']
    )


def create_daily_report_for_crem(form_value: Dict):
    daily_report_type = "日报"
    daily_report_time = "2024-04-22 00:00:00"
    daily_work_summary = "日报工作总结"
    daily_senders = "张华雪"
    daily_plans = ["明日计划1", "明日计划2", "明日计划3"]
    daily_result = crem_api_wrapper.add_daily_report(
        daily_report_type, daily_report_time, daily_work_summary,
        daily_senders,
        daily_plans
    )
    print("日报结果:", daily_result)
    return {}