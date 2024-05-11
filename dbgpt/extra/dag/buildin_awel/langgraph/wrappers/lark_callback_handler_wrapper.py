import time
from typing import Dict

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_api_wrapper, crem_daily_report_search, \
    crem_daily_report_id_search, card_send_daily_report_search
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_api_customer_visit
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_30DaysTrxTre_card

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_project_api_wrapper
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_project_requirement_search


from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import Day_30_TrxTre_card_tool
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import xxxxxx_card_send_requirement_search
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil


async def a_call(event: Dict):
    print("lark_callback_handler_wrapper_a_call", event)
    result = {}
    card_name = ""
    operator = event['operator']
    action = event['action']
    token = event['token']
    button_type = ""
    open_id = operator['open_id']
    union_id = operator['union_id']
    # open_id or union_id

    if "value" in action:
        action_value = action['value']
        if "card_name" in action_value:
            card_name = action_value['card_name']
        if "button_type" in action_value:
            button_type = action_value['button_type']
    if button_type == 'merchant_detail':
        customerNo = action['value']['customerNo']
        customerName = action['value']['customerName']
        conv_id = event['operator']['open_id']
        print('查询商户的编号', customerNo)
        result = Day_30_TrxTre_card_tool.user_crem_30DaysTrxTre_card(
            open_id=open_id,
            customer_id=customerNo,
            customerName=customerName,
            conv_id=conv_id)
    elif button_type == 'daily_report_detail':
        id = action['value']['id']
        report_time = action['value']['report_time']
        conv_id = event['operator']['open_id']
        print('查询日报的编号', id)
        print('对应销售的名称', report_time)
        result = card_send_daily_report_search.card_send_daily_report_search(
            open_id=open_id,
            report_id=id,
            report_time=report_time,
            conv_id=conv_id)
    if "form_value" not in action:
        # 非表单回调，按钮回调
        print("表单内容为空，跳过执行：", event)
        return result
    form_value = action['form_value']

    # 需求收集表单
    if card_name == "requirement_collect":
        result = create_requirement_for_lark_project(
            token=token, union_id=union_id, form_value=form_value
        )
    elif card_name == "daily_report_collect":
        result = create_daily_report_for_crem(
            open_id=open_id, form_value=form_value
        )
    elif card_name == "weekly_report_collect":
        result = create_weekly_report_for_crem(
            open_id=open_id, form_value=form_value
        )
    elif card_name == "customer_visit_record_collect":
        result = create_customer_visit_record_for_crem(
            open_id=open_id, form_value=form_value
        )
    elif card_name == 'crm_bus_customer_collect':
        result = create_crm_bus_customer_for_crem(
            open_id=open_id, form_value=form_value
        )
    # elif card_name == 'requirement_search':
    #     result = create_requirement_search_for_lark_project(
    #         token=token, union_id=union_id, form_value=form_value,event = event
    #     )
    # elif card_name == 'requirement_search_callback':
    #     result = card_send_requirement_callbacksearch(
    #         token=token, union_id=union_id, form_value=form_value
    #     )

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


def create_daily_report_for_crem(open_id, form_value: Dict):
    daily_report_type = "日报"
    daily_report_time = form_value['create_date'].split()[0] + " 00:00:00"
    daily_work_summary = form_value['daily_report_content']
    daily_plans = form_value['daily_report_tomorrow_plans']
    daily_result = crem_api_wrapper.add_daily_or_weekly_report(
        open_id=open_id,
        report_type=daily_report_type,
        report_time=daily_report_time,
        work_summary=daily_work_summary,
        plans=daily_plans
    )
    print("日报结果:", daily_result)
    print("开始更新日报卡片")

    return {}


def create_weekly_report_for_crem(open_id, form_value: Dict):
    daily_report_type = "周报"
    daily_report_time = form_value['create_date'].split()[0] + " 00:00:00"
    daily_work_summary = form_value['weekly_report_content']
    daily_plans = form_value['weekly_report_next_week_plans']
    daily_result = crem_api_wrapper.add_daily_or_weekly_report(
        open_id=open_id,
        report_type=daily_report_type,
        report_time=daily_report_time,
        work_summary=daily_work_summary,
        plans=daily_plans
    )
    print("周报结果:", daily_result)
    return {}


def create_customer_visit_record_for_crem(open_id, form_value: Dict):
    customer_name = form_value['customer_name']
    visit_date = form_value['visit_date'].split()[0] + " 00:00:00"
    visit_content = form_value['visit_content']
    visit_method = form_value['visit_method']
    visit_type = form_value['visit_type'],
    contacts = form_value['contacts']

    customer_visit_record = crem_api_customer_visit.add_customer_visit_record(
        open_id=open_id,
        customer_name=customer_name,
        followUpText=visit_content,
        followUpTime=visit_date,
        followUpTypeName=visit_method,
        visitTypeName=visit_type,
        contacts=contacts
    )

    print("拜访结果:", customer_visit_record)
    return {}

def create_crm_bus_customer_for_crem(open_id, form_value: Dict):
    customer_name = form_value['customer_name']
    customer_role = form_value['customer_role']
    customer_source = form_value['customer_source']
    customer_importance = form_value['customer_importance']
    sale_name = form_value['sale_name']
    industry_line = form_value['industry_line']
    business_type = form_value['business_type']

    # 大零售独有字段
    product_type = ''
    if industry_line == '大零售行业线':
        product_type = form_value['product_type']

    #政务行业线独有字段
    zw_client_assets = ''
    zw_business_type = ''
    zw_province = ''
    zw_system_vendor = ''
    zw_signed_annual_gross_profit = ''
    zw_customer_level = ''
    if industry_line == '政务行业线':
        zw_client_assets = form_value['zw_client_assets']
        zw_business_type = form_value['zw_business_type']
        zw_province = form_value['zw_province']
        zw_system_vendor = form_value['zw_system_vendor']
        zw_signed_annual_gross_profit = form_value['zw_signed_annual_gross_profit']
        zw_customer_level = form_value['zw_customer_level']


    customer_visit_record = crem_api_wrapper.add_crm_bus_customer(
        open_id=open_id,
        customer_name=customer_name,
        customer_role=customer_role,
        customer_source=customer_source,
        customer_importance=customer_importance,
        sale_name=sale_name,
        industry_line=industry_line,
        business_type=business_type,
        product_type=product_type,

        zw_client_assets=zw_client_assets,
        zw_business_type=zw_business_type,
        zw_province=zw_province,
        zw_system_vendor=zw_system_vendor,
        zw_signed_annual_gross_profit=zw_signed_annual_gross_profit,
        zw_customer_level=zw_customer_level

    )

    print("添加报单客户信息结果:", customer_visit_record)
    return {}

# def create_requirement_search_for_lark_project(token, event,union_id: str, form_value: Dict):
#     return card_send_requirement_search.card_send_requirement_callbacksearch(
#         conv_id=event['operator']['open_id'],
#         token=token,
#         project_key="ypgptapi",
#         union_id=union_id,
#         business_value=form_value['industry_line'],
#         priority_value=form_value['emergency_level'],
#         requirement_create_name=form_value['requirement_create_name']
#
#     )
