import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.util.lark import lark_card_util


class BookMeetingRoomToolInput(BaseModel):
    """
    我要预定一个会议室：

       - 期望预定日期：2024年5月2日
       - 会议室名称：极致
       - 会议开始时间：13:00
       - 会议结束时间：14:00

    """

    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    expected_date: str = Field(
        name="期望预定日期",
        description="期望预定日期",
        default=""
    )
    meeting_room_name: str = Field(
        name="会议室名称",
        description="会议室名称，" +
                    lark_card_util.card_options_to_input_field_description(
                        lark_card_util.card_options_for_meeting_room_name()
                    ),
        default=""
    )

    start_time: str = Field(
        name="会议开始时间",
        description="会议开始时间" +
                    lark_card_util.card_options_to_input_field_description(
                        lark_card_util.card_options_for_meeting_room_data()
                    ),
        default=""
    )
    end_time: str = Field(
        name="会议结束时间",
        description="会议结束时间" +
                    lark_card_util.card_options_to_input_field_description(
                        lark_card_util.card_options_for_meeting_room_data()
                    ),
        default=""
    )


class BookMeetingRoomTool(BaseTool):
    name: str = "book_meeting_room_tool"
    description: str = (
        "会议室预定工具，"
        "请注意：\n"
        "1、当需要预定会议室、创建日程、定会议室时非常有用。\n"
        "2、调用本工具需要的参数值来自用户输入，可以默认为空，但是禁止随意编造。\n"
        ""
    )
    args_schema: Type[BaseModel] = BookMeetingRoomToolInput

    def _run(
            self,
            conv_id: str = "",
            expected_date: str = "",
            meeting_room_name: str = "",
            start_time: str = "",
            end_time: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始运行客户拜访填写工具：", conv_id, expected_date, meeting_room_name, start_time, end_time)
        try:
            reuqires = []
            if expected_date == "":
                reuqires.append("expected_date")
            if meeting_room_name == "":
                reuqires.append("meeting_room_name")
            if start_time == "":
                reuqires.append("start_time")
            if end_time == "":
                reuqires.append("end_time")
            if len(reuqires) > 0:
                return {"success": "false", "response_message": "the description of " + "[" + ".".join(reuqires) + "]"}

            return handle(
                conv_id=conv_id,
                expected_date=expected_date,
                meeting_room_name=meeting_room_name,
                start_time=start_time,
                end_time=end_time
            )
        except Exception as e:
            logging.error("会议室查询预定工具运行异常：" + conv_id + " " + meeting_room_name, e)
            return repr(e)


def handle(
        conv_id: str,
        expected_date: str = "",
        meeting_room_name: str = "",
        start_time: str = "",
        end_time: str = ""

):
    try:
        return {
            "success": "true",
            "error_message": "",
            "action": {
                "action_name": "send_lark_form_card",
                "card_name": "book_meeting_room_collect"
            },
            "data": {
                "conv_id": conv_id,
                "expected_date": expected_date,
                "meeting_room_name": lark_card_util.get_action_index_by_text_from_options(
                    meeting_room_name,
                    lark_card_util.card_options_for_meeting_room_name()
                ),
                "meeting_room_names": lark_card_util.card_options_for_meeting_room_name(),
                "start_time": lark_card_util.get_action_index_by_text_from_options(
                    start_time,
                    lark_card_util.card_options_for_meeting_room_data()
                ),
                "start_times": lark_card_util.card_options_for_meeting_room_data(),
                "end_time": lark_card_util.get_action_index_by_text_from_options(
                    end_time,
                    lark_card_util.card_options_for_meeting_room_data()
                ),
                "end_times": lark_card_util.card_options_for_meeting_room_data()
            }
        }
    except Exception as e:
        raise Exception("跟进拜访数据组装失败：" + conv_id + " " + meeting_room_name, e)

#
#
#
