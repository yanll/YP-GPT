import logging
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple, Union

from dbgpt.agent.resource.resource_api import AgentResource

from .resource_api import ResourceClient, ResourceType

logger = logging.getLogger(__name__)


class ResourceLarkClient(ResourceClient):
    @property
    def type(self):
        return ResourceType.LarkApi

    def get_data_type(self, resource: AgentResource) -> str:
        return super().get_data_type(resource)

    async def get_data_introduce(
            self, resource: AgentResource, question: Optional[str] = None
    ) -> str:
        return await self.a_get_userinfo(resource.value, question)

    def get_all_meeting_rooms(
            self
    ) -> str:
        return '[{"capacity": 12,"floor_name": "F10","name": "Hacker","room_id": "omm_fce8075d5a6a25c764a808c69a48b82a"},{"capacity": 8,"floor_name": "F25","name": "smart","room_id": "omm_435bca3a3d40f120c63540028b965538"},{"capacity": 10,"floor_name": "F25","name": "think different","room_id": "omm_d511e9e4e40f68107f556c943ca50c44"},{"capacity": 90,"floor_name": "F23","name": "分享","room_id": "omm_2fa172ec56aba79c654ec5a4b58e9f27"},{"capacity": 12,"floor_name": "F10","name": "北极星","room_id": "omm_3864b3539c370d51e8d086791b008d44"},{"capacity": 8,"floor_name": "F10","name": "坦诚","room_id": "omm_247693a0dbb368b6af624c51ba5df218"},{"capacity": 4,"floor_name": "F10","name": "天权星","room_id": "omm_32be015ee6d9318e11561b984d665971"},{"capacity": 5,"floor_name": "F10","name": "天枢星","room_id": "omm_dcf65c2ffcbabe4bf01c72e0470c541b"},{"capacity": 7,"floor_name": "F10","name": "天狼星","room_id": "omm_7e99a24f850323e3038526ce3f809ba5"},{"capacity": 4,"floor_name": "F10","name": "天玑星","room_id": "omm_fecbfd6505548d491026365ad03cb215"},{"capacity": 5,"floor_name": "F10","name": "天璇星","room_id": "omm_ddee0861011df191f0404b80f0c7d9eb"},{"capacity": 5,"floor_name": "F10","name": "天衡星","room_id": "omm_e457d7a3eb7133f98fc27a267a1646c1"},{"capacity": 10,"floor_name": "F23","name": "太阳","room_id": "omm_d47dd4f223a3531f31b351513b036f61"},{"capacity": 31,"floor_name": "F23","name": "尽责","room_id": "omm_41510695cc2c9e86c3ef7d4afc247c74"},{"capacity": 6,"floor_name": "F23","name": "开放","room_id": "omm_9da759bfae9935249eda2ce675e2682e"},{"capacity": 6,"floor_name": "F10","name": "开阳星","room_id": "omm_56bb92f696093b60a3108ae3b7102a78"},{"capacity": 6,"floor_name": "F10","name": "摇光星","room_id": "omm_2db12593ce9242345be73a59a0120ccc"},{"capacity": 7,"floor_name": "F25","name": "敢干","room_id": "omm_4a260a86bc05a2d7dbb901c53bf5bc92"},{"capacity": 5,"floor_name": "F10","name": "敢想","room_id": "omm_001832945aef034f5853ca649db51b97"},{"capacity": 15,"floor_name": "F10","name": "敢说","room_id": "omm_5a1d13dc13e79e6f739b3d6f2d26c452"},{"capacity": 10,"floor_name": "F25","name": "敢败","room_id": "omm_1898ce77b933009c84cc999a93aeefc4"},{"capacity": 8,"floor_name": "F25","name": "极致","room_id": "omm_a77aef5161de2d637bc0c156647474d4"},{"capacity": 4,"floor_name": "F10","name": "泰山","room_id": "omm_bb38d0046d5159a31385030a1346a6c5"},{"capacity": 12,"floor_name": "F10","name": "浪漫","room_id": "omm_a5ec3a14a94322968cd6fea05b34f4df"},{"capacity": 6,"floor_name": "F23","name": "禾口","room_id": "omm_e8f296a80f0f448a9d6c659abb0a7ea8"},{"capacity": 6,"floor_name": "F23","name": "蓝点","room_id": "omm_c520c17858b4b6fb22bac99f6e1dda5b"},{"capacity": 5,"floor_name": "F10","name": "超越","room_id": "omm_9ca36d25bfe178df5da26205b39da278"}]'

    def get_meeting_room_status(
            self
    ) -> str:
        return self.get_meeting_room_status()

    async def a_get_userinfo(self, db: str, question: Optional[str] = None) -> str:
        raise NotImplementedError("The run method should be implemented in a subclass.")

    async def a_muti_table_add_record(self, app_id: str, table_id: str, record: dict) -> None:
        raise NotImplementedError("The run method should be implemented in a subclass.")

    async def a_lark_after_notify(self, receive_id: str, text: str):
        raise NotImplementedError("The run method should be implemented in a subclass.")

    async def get_meeting_room_status(self):
        raise NotImplementedError("The run method should be implemented in a subclass.")

    async def create_calendar(self, title, name, room_id, start_time, end_time):
        raise NotImplementedError("The run method should be implemented in a subclass.")


class MockResourceLarkClient(ResourceLarkClient):
    pass
