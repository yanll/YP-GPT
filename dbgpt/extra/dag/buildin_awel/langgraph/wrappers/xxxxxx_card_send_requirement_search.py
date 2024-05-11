# import json
#
# from dbgpt.extra.dag.buildin_awel.lark import card_templates
# from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.lark_project_requirement_search import create_requirement_search_for_lark_project
# from dbgpt.util.lark import lark_message_util
# import logging
#
# def card_send_requirement_callbacksearch(union_id,
#                                          token,
#                                          requirement_create_name,
#                                          project_key,
#                                          business_value=None,
#                                          priority_value=None,
#                                          conv_id=None):
#
#     global bus_id
#     try:
#         if business_value == "":
#             # 日报ID为空，返回错误消息
#             return {"success": False, "response_message": "行业线不能为空"}
#
#         # 调用外部函数获取商户信息分析结果
#         else:
#             requirement_search_analysis = create_requirement_search_for_lark_project(
#                     token,
#                     requirement_create_name,
#                     project_key,
#                     union_id,
#                     business_value,
#                     priority_value
#                     ),
#             print("完整返回结果", requirement_search_analysis)
#             extracted_info,priority_label= requirement_search_analysis[0]
#             print("需求查询返回结果",extracted_info)
#
#             # 构建行业线编号到实际名称的映射字典
#             industry_line_map = {
#                 "662db530cde8ed174622a08d": "航旅行业线",
#                 "662db56afe2c0b51b33668eb": "大零售行业线",
#                 "662db596fe2c0b51b33668ec": "线上线下一体化",
#                 "662db5b688aa18a943e64644": "老板管账",
#                 "662db5c3a55775e2c9c83bf9": "金融行业线"
#             }
#
#             # 替换业务线编号为实际名称
#             for item in extracted_info:
#                 business_id = item.get("business_id", "")
#                 if business_id in industry_line_map:
#                     item["business_id"] = industry_line_map[business_id]
#                     bus_id = item["business_id"]
#
#             resp_data = {}
#             resp_data = extracted_info
#
#         query_str = (
#                 "行业线：" + bus_id + "\n"
#                 "紧急程度:" + priority_label + "\n"
#                 "需求创建人:" + requirement_create_name
#         ).strip()
#         print("需求池详情查询结果：", query_str, resp_data)
#         display_type = ""
#         list = []
#         if resp_data and len(resp_data) > 0:
#             for m in resp_data:
#                 name = m.get("name", "")
#                 exp_time = m.get("exp_time", "")
#                 priority_label = m.get("priority_label", "")
#                 business_id = m.get("business_id", "")
#                 start_time = m.get("start_time", "")
#                 owner = m.get("owner", "")
#
#                 list.append({
#                     "owner": owner if owner is not None else "",
#                     "start_time": start_time if start_time is not None else "",
#                     "business_id": business_id if business_id is not None else "",
#                     "priority_label": priority_label if priority_label is not None else "",
#                     "exp_time": exp_time if exp_time is not None else "",
#                     "name": name if name is not None else ""
#                 })
#             display_type = "form"
#             lark_message_util.send_message(
#                 receive_id=conv_id,
#                 content=card_templates.requirement_search_list_card_content(
#                     template_variable={
#                         "query_str": query_str,
#                         "requirement_search_list": list
#                     }
#                 ),
#                 receive_id_type="open_id",
#                 msg_type="interactive"
#             )
#         return {
#                 "success": "true",
#                 "error_message": "",
#                 "display_type": display_type,
#                 "data": list
#             }
#     except Exception as e:
#             logging.error("需求查询工具运行异常：", e)
#             return repr(e)
#
#
