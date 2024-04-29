import time
from typing import Dict

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_api_wrapper
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_api_customer_visit

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_project_api_wrapper
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil


async def a_call(event: Dict):
    print("lark_callback_handler_wrapper_a_call", event)
    result = {}
    card_name = ""
    operator = event['operator']
    action = event['action']
    token = event['token']
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
            token=token, union_id=union_id, form_value=form_value
        )
    elif card_name == "daily_report_collect":
        result = create_daily_report_for_crem(
            form_value=form_value, token=token
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


def create_requirement_for_lark_project(token, union_id: str, form_value: Dict):
    return lark_project_api_wrapper.create_requirement_for_lark_project(
        token=token,
        project_key="ypgptapi",
        union_id=union_id,
        name=form_value['requirement_content'],
        business_value=form_value['industry_line'],
        priority_value=form_value['emergency_level'],
        expected_time=form_value['expected_completion_date']
    )


def create_daily_report_for_crem(form_value: Dict, token: str):
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
    print("开始更新日报卡片")
    # larkutil.send_interactive_update_message(
    #     token=token,
    #     content=card_templates.create_interactive_update_daily_report_card_content(
    #         template_variable={
    #             "card_metadata": {
    #                 "card_name": "interactive_update_daily_report_collect",
    #                 "description": "交互更新日报收集表单"
    #             },
    #             "daily_report_tomorrow_plans": daily_plans,
    #             "create_date": daily_report_time.split()[0],
    #             "daily_report_content": daily_work_summary,
    #
    #         }
    #     ),
    # )

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
    customer_name = form_value['customer_name']
    visit_date = form_value['visit_date'].split()[0] + " 00:00:00"
    visit_content = form_value['visit_content']
    visit_method = form_value['visit_method']
    visit_type = form_value['visit_type'],
    contacts = form_value['contacts']

    customer_visit_record = crem_api_customer_visit.add_customer_visit_record(
        customer_name=customer_name,
        followUpText=visit_content,
        followUpTime=visit_date,
        followUpTypeName=visit_method,
        visitTypeName=visit_type,
        contacts=contacts
    )

    print("拜访结果:", customer_visit_record)
    return {}
