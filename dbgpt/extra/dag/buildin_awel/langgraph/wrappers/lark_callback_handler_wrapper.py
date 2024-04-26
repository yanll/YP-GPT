from typing import Dict

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_api_wrapper
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_api_customer_visit

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_project_api_wrapper


async def a_call(event: Dict):
    print("lark_callback_handler_wrapper_a_call", event)
    result = {}
    card_name = ""
    operator = event['operator']
    action = event['action']
    if "value" in action:
        action_value = action['value']
        if "card_name" in action_value:
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
    elif card_name == "weekly_report_collect":
        result = create_weekly_report_for_crem(
            form_value=form_value
        )
    elif card_name == "customer_visit_record_collect":
        result = create_customer_visit_record_for_crem(
            form_value=form_value
        )
    print("lark_callback_handler_wrapper_a_call_result:", result)
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
    daily_report_time = form_value['create_date'].split()[0] + " 00:00:00"
    daily_work_summary = form_value['daily_report_content']
    daily_plans = form_value['daily_report_tomorrow_plans']
    daily_result = crem_api_wrapper.add_daily_or_weekly_report(
        report_type=daily_report_type,
        report_time=daily_report_time,
        work_summary=daily_work_summary,
        plans=daily_plans
    )
    print("日报结果:", daily_result)
    return {}


def create_weekly_report_for_crem(form_value: Dict):
    daily_report_type = "周报"
    daily_report_time = form_value['create_date'].split()[0] + " 00:00:00"
    daily_work_summary = form_value['weekly_report_content']
    daily_plans = form_value['weekly_report_next_week_plans']
    daily_result = crem_api_wrapper.add_daily_or_weekly_report(
        report_type=daily_report_type,
        report_time=daily_report_time,
        work_summary=daily_work_summary,
        plans=daily_plans
    )
    print("周报结果:", daily_result)
    return {}


def create_customer_visit_record_for_crem(form_value: Dict):
    customer_name = "测试商户"
    visit_method = "电话拜访",
    visit_type = "初次拜访"
    visit_content = "拜访内容测试"
    visit_date = "2024-04-25 00:00:00"
    customer_visit_record = crem_api_customer_visit.add_customer_visit_record(customer_name, visit_content, visit_date,
                                                                              visit_method, visit_type)

    print("日报结果:", customer_visit_record)
    return {}
