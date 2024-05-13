import logging
from typing import Optional, Type
from typing import List

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.crem_api_wrapper import get_crm_user_industry_line, \
    get_crm_user_name
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import lark_message_util, lark_card_util


class CrmBusCustomerCollectInput(BaseModel):
    """

    """
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    customer_name: str = Field(
        name="客户名称",
        description="客户名称",
        default=""
    )

    # industry_line: str = Field(
    #     name="行业线",
    #     description="行业线， " + lark_card_util.card_options_to_input_field_description(
    #         lark_card_util.card_options_for_industry_line()
    #     ),
    #     default=""
    # )
    business_type: str = Field(
        name="所属行业",
        description="所属行业",
        default=""
    )

    air_travel_business_type: str = Field(
        name="所属行业的分类",
        description=lark_card_util.card_options_for_business_type.AirTravel.description(),
        default=""
    )

    customer_role: str = Field(
        name='客户角色',
        description='客户角色，' + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_customer_role()
        ),
    )
    customer_source_default: str = Field(
        name="客户来源",
        description="客户来源, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_customer_source()
        ),
        default=""
    )
    customer_importance_default: str = Field(
        name="客户重要程度",
        description="客户重要程度, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_customer_importance()
        ),
        default=""
    )

    # 大零售特有字段
    product_type: str = Field(
        name="产品形态",
        description="产品形态, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_product_type()
        ),
        default=""
    )

    # 政务行业线特有字段
    zw_client_assets: str = Field(
        name="客户资产",
        description="客户资产, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_zw_client_assets()
        ),
        default=""
    )
    zw_business_type: str = Field(
        name="业务类型",
        description="业务类型, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_zw_business_type()
        ),
        default=""
    )
    zw_province: str = Field(
        name="省份",
        description="省份, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_zw_province()
        ),
        default=""
    )
    zw_system_vendor: str = Field(
        name="系统商",
        description="系统商",
        default=""
    )
    zw_signed_annual_gross_profit: str = Field(
        name="签约年毛利(万元)",
        description="签约年毛利(万元)",
        default=""
    )
    zw_customer_level: str = Field(
        name="省份",
        description="省份, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_zw_customer_level()
        ),
        default=""
    )

    # 航旅事业部特有字段
    customer_size: str = Field(
        name="客户规模",
        description="客户规模, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_customer_size()
        ),
        default=""
    )
    customer_profile: str = Field(
        name="客户业务描述",
        description="客户业务描述",
        default=""
    )
    important_step: str = Field(
        name="客户所处阶段",
        description="客户所处阶段, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_important_step()
        ),
        default=""
    )
    # 航旅第二类特有字段
    purchasing_channels: str = Field(
        name="采购渠道",
        description="采购渠道, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_purchasing_channels()
        ),
        default=""
    )
    payment_scene: str = Field(
        name="支付场景",
        description="支付场景, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_payment_scene()
        ),
        default=""
    )
    sales_channel: str = Field(
        name="销售渠道",
        description="销售渠道, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_sales_channel()
        ),
        default=""
    )


class CrmBusCustomerCollectAddTool(BaseTool):
    name: str = "crm_bus_customer_collect_tool"
    description: str = (
        "这是一个填写报单的工具，帮助用户填写报单。"
        "当需要填写报单客户时非常有用。 "
        "能够尽可能全的收集报单信息。"
        "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
        ""
    )
    args_schema: Type[BaseModel] = CrmBusCustomerCollectInput

    def _run(
            self,
            conv_id: str = "",
            customer_name: str = "",
            industry_line: str = "",
            business_type: str = "",
            customer_role: str = "",
            customer_source_default: str = "",
            customer_importance_default: str = "",
            # 大零售
            product_type: str = "",
            # 政务
            zw_client_assets: str = "",
            zw_business_type: str = "",
            zw_province: str = "",
            zw_system_vendor: str = "",
            zw_signed_annual_gross_profit: str = "",
            zw_customer_level: str = "",

            # 航旅特有字段
            customer_size: str = "",
            customer_profile: str = "",
            air_travel_business_type: str = "",
            important_step: str = "",
            purchasing_channels: str = "",
            payment_scene: str = "",
            sales_channel: str = "",

    ):
        """Use the tool."""
        print("开始运行添加报单客户信息填写工具：", conv_id, customer_name, customer_role, customer_source_default,
              customer_importance_default)
        try:
            industry_line = get_crm_user_industry_line(open_id=conv_id)
            crem_user_name = get_crm_user_name(open_id=conv_id)
            if industry_line == "":
                resp = {"success": "false", "response_message": "该用户无行业线"}
            elif crem_user_name == "":
                resp = {"success": "false", "response_message": "该用户无CREM系统权限"}
            elif industry_line == "航旅事业部" and air_travel_business_type not in ['第一类', '第二类']:
                resp = {"success": "false", "response_message": "请告诉我所属行业的类型。"}
            else:
                resp = do_collect(
                    conv_id=conv_id,
                    industry_line=industry_line,
                    business_type=business_type,
                    customer_name=customer_name,
                    customer_role=customer_role,
                    customer_source_default=customer_source_default,
                    customer_importance_default=customer_importance_default,
                    product_type=product_type,
                    crem_user_name=crem_user_name,
                    air_travel_business_type=air_travel_business_type,

                    zw_client_assets=zw_client_assets,
                    zw_business_type=zw_business_type,
                    zw_province=zw_business_type,
                    zw_system_vendor=zw_system_vendor,
                    zw_signed_annual_gross_profit=zw_signed_annual_gross_profit,
                    zw_customer_level=zw_customer_level,

                    important_step=important_step,
                    customer_size=customer_size,
                    customer_profile=customer_profile,
                    purchasing_channels=purchasing_channels,
                    payment_scene=payment_scene,
                    sales_channel=sales_channel,

                )
            return resp
        except Exception as e:
            logging.error("工具运行异常：", e)
            return repr(e)


def do_collect(
        conv_id: str = "",
        customer_name: str = "",
        industry_line: str = "",
        business_type: str = "",
        customer_role: str = "",
        customer_source_default: str = "",
        customer_importance_default: str = "",
        product_type: str = "",
        crem_user_name: str = '',
        air_travel_business_type: str = '',
        zw_client_assets: str = "",
        zw_business_type: str = "",
        zw_province: str = "",
        zw_system_vendor: str = "",
        zw_signed_annual_gross_profit: str = "",
        zw_customer_level: str = "",

        important_step: str = "",
        customer_size: str = "",
        customer_profile: str = "",
        purchasing_channels: str = "",
        payment_scene: str = "",
        sales_channel: str = "",
):
    """
    处理并收集提报信息，返回收集结果。
    """
    try:
        """
        我要填写报单客户：
        客户名：转转精神。
        客户角色：标准商户
        客户来源：朋友介绍
        客户重要程度：一般商户
        """
        print("发送飞书提报卡片：", conv_id)
        if industry_line == "Web3.0行业线" or industry_line == "外综服行业线" or industry_line == "大出行项目组":
            business_type = ''
            if industry_line == "Web3.0行业线":
                business_type = 'Web3.0'
            elif industry_line == "外综服行业线":
                business_type = '外综服'
            elif industry_line == "大出行项目组":
                business_type = '其他'

            content = card_templates.create_crm_bus_customer_card_content.Web3_or_ForeignComprehensiveService(
                template_variable={
                    "card_metadata": {
                        "card_name": "crm_bus_customer_collect",
                        "card_description": "添加报单客户信息表单"
                    },
                    "industry_line": industry_line,
                    "customer_name": customer_name,
                    "business_type": business_type,
                    "customer_role": lark_card_util.get_action_index_by_text_from_options(
                        customer_role,
                        lark_card_util.card_options_for_customer_role()
                    ),
                    "customer_source_default": lark_card_util.get_action_index_by_text_from_options(
                        customer_source_default,
                        lark_card_util.card_options_for_customer_source()
                    ),
                    "customer_importance_default": lark_card_util.get_action_index_by_text_from_options(
                        customer_importance_default,
                        lark_card_util.card_options_for_customer_importance()
                    ),
                    "crem_user_name": crem_user_name,

                    "customer_role_options": lark_card_util.card_options_for_customer_role(),
                    "customer_source_options": lark_card_util.card_options_for_customer_source(),
                    "customer_importance_options": lark_card_util.card_options_for_customer_importance()
                }
            )

        elif industry_line == "金融行业线" or industry_line == "跨境行业线":
            business_type_options = []
            if industry_line == "金融行业线":
                business_type_options = lark_card_util.card_options_for_business_type.Finance()
            elif industry_line == "跨境行业线":
                business_type_options = lark_card_util.card_options_for_business_type.CrossBorder()

            content = card_templates.create_crm_bus_customer_card_content.Finance_or_CrossBorder(
                template_variable={
                    "card_metadata": {
                        "card_name": "crm_bus_customer_collect",
                        "card_description": "添加报单客户信息表单"
                    },
                    "industry_line": industry_line,
                    "customer_name": customer_name,
                    "business_type": lark_card_util.get_action_index_by_text_from_options(
                        business_type,
                        business_type_options
                    ),
                    "customer_role": lark_card_util.get_action_index_by_text_from_options(
                        customer_role,
                        lark_card_util.card_options_for_customer_role()
                    ),
                    "customer_source_default": lark_card_util.get_action_index_by_text_from_options(
                        customer_source_default,
                        lark_card_util.card_options_for_customer_source()
                    ),
                    "customer_importance_default": lark_card_util.get_action_index_by_text_from_options(
                        customer_importance_default,
                        lark_card_util.card_options_for_customer_importance()
                    ),
                    "crem_user_name": crem_user_name,
                    "business_type_options": business_type_options,
                    "customer_role_options": lark_card_util.card_options_for_customer_role(),
                    "customer_source_options": lark_card_util.card_options_for_customer_source(),
                    "customer_importance_options": lark_card_util.card_options_for_customer_importance()
                }
            )

        elif industry_line == "大零售行业线":

            content = card_templates.create_crm_bus_customer_card_content.Retail(
                template_variable={
                    "card_metadata": {
                        "card_name": "crm_bus_customer_collect",
                        "card_description": "添加报单客户信息表单"
                    },
                    "customer_name": customer_name,
                    "business_type": lark_card_util.get_action_index_by_text_from_options(
                        business_type,
                        lark_card_util.card_options_for_business_type.Retail(),
                    ),
                    "customer_role": lark_card_util.get_action_index_by_text_from_options(
                        customer_role,
                        lark_card_util.card_options_for_customer_role()
                    ),
                    "customer_source_default": lark_card_util.get_action_index_by_text_from_options(
                        customer_source_default,
                        lark_card_util.card_options_for_customer_source()
                    ),
                    "customer_importance_default": lark_card_util.get_action_index_by_text_from_options(
                        customer_importance_default,
                        lark_card_util.card_options_for_customer_importance()
                    ),

                    "product_type": lark_card_util.get_action_index_by_text_from_options(
                        product_type,
                        lark_card_util.card_options_for_product_type()
                    ),
                    "crem_user_name": crem_user_name,
                    "business_type_options": lark_card_util.card_options_for_business_type.Retail(),
                    "customer_role_options": lark_card_util.card_options_for_customer_role(),
                    "customer_source_options": lark_card_util.card_options_for_customer_source(),
                    "customer_importance_options": lark_card_util.card_options_for_customer_importance(),
                    "product_type_options": lark_card_util.card_options_for_product_type()
                }
            )

        elif industry_line == "政务行业线":
            business_type_options = lark_card_util.card_options_for_business_type.Government()

            content = card_templates.create_crm_bus_customer_card_content.Government(
                template_variable={
                    "card_metadata": {
                        "card_name": "crm_bus_customer_collect",
                        "card_description": "添加报单客户信息表单"
                    },
                    "industry_line": industry_line,

                    "customer_name": customer_name,
                    "business_type": lark_card_util.get_action_index_by_text_from_options(
                        business_type,
                        lark_card_util.card_options_for_business_type.Government(),
                    ),
                    "customer_role": lark_card_util.get_action_index_by_text_from_options(
                        customer_role,
                        lark_card_util.card_options_for_customer_role()
                    ),
                    "customer_source_default": lark_card_util.get_action_index_by_text_from_options(
                        customer_source_default,
                        lark_card_util.card_options_for_customer_source()
                    ),
                    "customer_importance_default": lark_card_util.get_action_index_by_text_from_options(
                        customer_importance_default,
                        lark_card_util.card_options_for_customer_importance()
                    ),
                    "zw_client_assets": lark_card_util.get_action_index_by_text_from_options(
                        zw_client_assets,
                        lark_card_util.card_options_for_zw_client_assets()
                    ),
                    "zw_business_type": lark_card_util.get_action_index_by_text_from_options(
                        zw_business_type,
                        lark_card_util.card_options_for_zw_business_type()
                    ),
                    "zw_province": lark_card_util.get_action_index_by_text_from_options(
                        zw_province,
                        lark_card_util.card_options_for_zw_province()
                    ),
                    'zw_system_vendor': zw_system_vendor,
                    'zw_signed_annual_gross_profit': zw_signed_annual_gross_profit,
                    "zw_customer_level": lark_card_util.get_action_index_by_text_from_options(
                        zw_customer_level,
                        lark_card_util.card_options_for_zw_customer_level()
                    ),

                    "crem_user_name": crem_user_name,
                    "business_type_options": business_type_options,
                    "customer_role_options": lark_card_util.card_options_for_customer_role(),
                    "customer_source_options": lark_card_util.card_options_for_customer_source(),
                    "customer_importance_options": lark_card_util.card_options_for_customer_importance(),
                    "zw_client_assets_options": lark_card_util.card_options_for_zw_client_assets(),
                    "zw_business_type_options": lark_card_util.card_options_for_zw_business_type(),
                    "zw_province_options": lark_card_util.card_options_for_zw_province(),
                    "zw_customer_level_options": lark_card_util.card_options_for_zw_customer_level(),
                }
            )

        elif industry_line == "航旅事业部":
            if air_travel_business_type == '第一类':

                content = card_templates.create_crm_bus_customer_card_content.AirTravel.Category_I(
                    template_variable={
                        "card_metadata": {
                            "card_name": "crm_bus_customer_collect",
                            "description": "添加报单客户信息表单"
                        },
                        "industry_line": industry_line,
                        "customer_name": customer_name,
                        "customer_size": lark_card_util.get_action_index_by_text_from_options(
                            customer_size,
                            lark_card_util.card_options_for_customer_size(),
                        ),
                        "customer_profile": customer_profile,
                        "business_type": lark_card_util.get_action_index_by_text_from_options(
                            business_type,
                            lark_card_util.card_options_for_business_type.AirTravel.Category_I(),
                        ),
                        "customer_role": lark_card_util.get_action_index_by_text_from_options(
                            customer_role,
                            lark_card_util.card_options_for_customer_role()
                        ),
                        "customer_source_default": lark_card_util.get_action_index_by_text_from_options(
                            customer_source_default,
                            lark_card_util.card_options_for_customer_source()
                        ),
                        "customer_importance_default": lark_card_util.get_action_index_by_text_from_options(
                            customer_importance_default,
                            lark_card_util.card_options_for_customer_importance()
                        ),
                        "important_step": lark_card_util.get_action_index_by_text_from_options(
                            important_step,
                            lark_card_util.card_options_for_customer_importance(),
                        ),
                        "crem_user_name": crem_user_name,

                        "business_type_options": business_type_options,
                        "customer_role_options": lark_card_util.card_options_for_customer_role(),
                        "customer_source_options": lark_card_util.card_options_for_customer_source(),
                        "customer_importance_options": lark_card_util.card_options_for_customer_importance(),
                        "customer_size_options": lark_card_util.card_options_for_customer_size(),

                        "important_step_options": lark_card_util.card_options_for_important_step()
                    }
                )

            else:
                business_type_options = lark_card_util.card_options_for_business_type.AirTravel.Category_II()

                content = card_templates.create_crm_bus_customer_card_content.AirTravel.Category_II(
                    template_variable={
                        "card_metadata": {
                            "card_name": "crm_bus_customer_collect",
                            "description": "添加报单客户信息表单"
                        },
                        "industry_line": industry_line,
                        "customer_name": customer_name,
                        "customer_size": lark_card_util.get_action_index_by_text_from_options(
                            customer_size,
                            lark_card_util.card_options_for_customer_size(),
                        ),
                        "customer_profile": customer_profile,
                        "business_type": lark_card_util.get_action_index_by_text_from_options(
                            business_type,
                            lark_card_util.card_options_for_business_type.AirTravel.Category_II(),
                        ),
                        "customer_role": lark_card_util.get_action_index_by_text_from_options(
                            customer_role,
                            lark_card_util.card_options_for_customer_role()
                        ),
                        "customer_source_default": lark_card_util.get_action_index_by_text_from_options(
                            customer_source_default,
                            lark_card_util.card_options_for_customer_source()
                        ),
                        "customer_importance_default": lark_card_util.get_action_index_by_text_from_options(
                            customer_importance_default,
                            lark_card_util.card_options_for_customer_importance()
                        ),
                        "important_step": lark_card_util.get_action_index_by_text_from_options(
                            important_step,
                            lark_card_util.card_options_for_customer_importance(),
                        ),
                        "purchasing_channels": lark_card_util.get_action_index_by_text_from_options(
                            purchasing_channels,
                            lark_card_util.card_options_for_purchasing_channels()
                        ),
                        "payment_scene": lark_card_util.get_action_index_by_text_from_options(
                            payment_scene,
                            lark_card_util.card_options_for_payment_scene()
                        ),
                        "sales_channel": lark_card_util.get_action_index_by_text_from_options(
                            sales_channel,
                            lark_card_util.card_options_for_sales_channel()
                        ),
                        "crem_user_name": crem_user_name,

                        "business_type_options": business_type_options,
                        "customer_role_options": lark_card_util.card_options_for_customer_role(),
                        "customer_source_options": lark_card_util.card_options_for_customer_source(),
                        "customer_importance_options": lark_card_util.card_options_for_customer_importance(),
                        "customer_size_options": lark_card_util.card_options_for_customer_size(),
                        "important_step_options": lark_card_util.card_options_for_important_step(),
                        "purchasing_channels_options": lark_card_util.card_options_for_purchasing_channels(),
                        "payment_scene_options": lark_card_util.card_options_for_payment_scene(),
                        'sales_channel_options': lark_card_util.card_options_for_sales_channel(),
                    }
                )

        # 没有行业线表单
        else:
            return {"success": "false", "response_message": "无报单权限"}
        content['data']['template_variable']['submit_callback_event'] = {
            "event_type": "submit",
            "event_source": 'crm_bus_customer_collect'
        }
        content['data']['template_variable']['unlike_callback_event'] = {
            "event_type": "unlike",
            "event_source": 'crm_bus_customer_collect',
            "event_data": {
                "message": "填写报单"
            }
        }
        return {
            "success": "true",
            "error_message": "",
            "action": {
                "action_name": "send_lark_form_card",
                "card_name": "crm_bus_customer_collect"
            },
            "data": {
                "conv_id": conv_id,
                "content": content

            }
        }


    except Exception as e:
        logging.error("飞书添加报单客户信息卡片发送失败：", e)

    # 创建并返回结果字典
