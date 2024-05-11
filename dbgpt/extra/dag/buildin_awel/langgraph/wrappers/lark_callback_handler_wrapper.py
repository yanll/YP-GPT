import asyncio
import logging
from typing import Dict

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import Day_30_TrxTre_card_tool
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_api_customer_visit
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_api_wrapper, card_send_daily_report_search
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_project_api_wrapper
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import lark_card_util, lark_message_util


async def a_call(app_chat_service, event: Dict):
    print("lark_callback_handler_wrapper_a_call", event)
    operator = event['operator']
    action = event['action']
    action_value = None
    token = event['token']
    event_type = ""
    event_source = ""
    event_data = None
    open_id = operator['open_id']
    union_id = operator['union_id']

    if "action" in event:
        action = event['action']
        action_value = action['value']
        if "event_type" in action_value:
            event_type = action_value["event_type"]
        if "event_source" in action_value:
            event_source = action_value["event_source"]
        if "event_data" in action_value:
            event_data = action_value["event_data"]

    if event_type == "":
        logging.info("事件为空，跳过执行：" + str(event))

    if event_type == "new_chat":
        return do_new_chat(app_chat_service, open_id)

    if event_type == "like":
        return do_like(app_chat_service, open_id, event["context"]["open_message_id"])

    if event_type == "unlike":
        message = ""
        if event_data and "message" in event_data:
            message = event_data["message"]
        return do_unlike(app_chat_service, open_id, event["context"]["open_message_id"], message)

    if event_type == "submit":
        form_value = action['form_value']
        # 需求收集表单
        if event_source == "requirement_collect":
            return create_requirement_for_lark_project(
                token=token, union_id=union_id, form_value=form_value
            )
        if event_source == "daily_report_collect":
            return create_daily_report_for_crem(
                open_id=open_id, form_value=form_value
            )
        if event_source == "weekly_report_collect":
            return create_weekly_report_for_crem(
                open_id=open_id, form_value=form_value
            )
        if event_source == "customer_visit_record_collect":
            return create_customer_visit_record_for_crem(
                open_id=open_id, form_value=form_value
            )
        if event_source == 'crm_bus_customer_collect':
            return create_crm_bus_customer_for_crem(
                open_id=open_id, form_value=form_value
            )
        if event_source == 'comment_collect':
            print(str(event_data))
            print(str(form_value))
        return {}

    if event_type == 'merchant_detail':
        customerNo = action_value['customerNo']
        customerName = action_value['customerName']
        print('查询商户的编号', customerNo)
        return Day_30_TrxTre_card_tool.user_crem_30DaysTrxTre_card(
            open_id=open_id,
            customer_id=customerNo,
            customerName=customerName,
            conv_id=open_id)

    if event_type == 'daily_report_detail':
        id = action['value']['id']
        report_time = action['value']['report_time']
        conv_id = event['operator']['open_id']
        print('查询日报的编号', id)
        print('对应销售的名称', report_time)
        return card_send_daily_report_search.card_send_daily_report_search(
            open_id=open_id,
            report_id=id,
            report_time=report_time,
            conv_id=conv_id)
    return {}


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

    # 政务行业线独有字段
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

    # 航旅行业线独有字段
    important_step = ''
    if industry_line == '航旅事业部':
        important_step = form_value['important_step']
    # 航旅中第二类
    purchasing_channels = ''
    payment_scene = ''
    sales_channel = ''
    if industry_line == '航旅事业部' and 'sales_channel' in form_value:
        purchasing_channels_raw = form_value['purchasing_channels']
        purchasing_channels = [purchasing_channels_raw.split(':')[0], purchasing_channels_raw.split(':')[-1]]
        payment_scene = form_value['payment_scene']
        sales_channel = form_value['sales_channel']

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
        zw_customer_level=zw_customer_level,

        important_step=important_step,
        purchasing_channels=purchasing_channels,
        payment_scene=payment_scene,
        sales_channel=sales_channel,
    )

    print("添加报单客户信息结果:", customer_visit_record)
    return {}


def do_new_chat(app_chat_service, open_id):
    asyncio.create_task(
        app_chat_service.a_disable_app_chat_his_message_by_uid(open_id)
    )
    lark_card_util.send_message_with_welcome(
        receive_id=open_id,
        template_variable={
            "message_content": "已开启新会话！"
        }
    )
    return {}


def do_like(app_chat_service, open_id, open_message_id):
    app_chat_service.a_update_app_chat_his_message_like_by_uid_mid(
        comment_type="like", conv_uid=open_id,
        message_id=open_message_id
    )
    return {
        "toast": {
            "type": "info",
            "content": "温馨提示",
            "i18n": {
                "zh_cn": "感谢您的点赞！",
                "en_us": "submitted"
            }
        }
    }


def do_unlike(app_chat_service, open_id, open_message_id, message):
    app_chat_service.a_update_app_chat_his_message_like_by_uid_mid(
        comment_type="unlike", conv_uid=open_id,
        message_id=open_message_id
    )

    lark_message_util.send_card_message(
        receive_id=open_id,
        content=card_templates.comment_card_content(
            template_variable={
                "submit_callback_event": {
                    "event_type": "submit",
                    "event_source": "comment_collect",
                    "event_data": {
                        "original_message_id": open_message_id
                    }
                },
                "open_message_id": open_message_id,
                "message": message
            }
        )
    )

    return {
        "toast": {
            "type": "info",
            "content": "温馨提示",
            "i18n": {
                "zh_cn": "感谢您的反馈，我们会努力改进哦！",
                "en_us": "submitted"
            }
        }
    }
