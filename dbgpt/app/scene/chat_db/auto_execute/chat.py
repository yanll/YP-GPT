from typing import Dict
import logging
from dbgpt._private.config import Config
from dbgpt.agent.util.api_call import ApiCall
from dbgpt.app.scene import BaseChat, ChatScene
from dbgpt.util.executor_utils import blocking_func_to_async
from dbgpt.util.tracer import root_tracer, trace
from dbgpt.util import envutils
CFG = Config()

logger = logging.getLogger(__name__)
class ChatWithDbAutoExecute(BaseChat):
    chat_scene: str = ChatScene.ChatWithDbExecute.value()

    """Number of results to return from the query"""

    def __init__(self, chat_param: Dict):
        """Chat Data Module Initialization
        Args:
           - chat_param: Dict
            - chat_session_id: (str) chat session_id
            - current_user_input: (str) current user input
            - model_name:(str) llm model name
            - select_param:(str) dbname
        """
        
        chat_mode = ChatScene.ChatWithDbExecute
        self.db_name = chat_param["select_param"]
        self.table_name = chat_param["table_name"] if chat_param.get("table_name") is not None else None
        chat_param["chat_mode"] = chat_mode
        """ """
        super().__init__(
            chat_param=chat_param,
        )
        if not self.db_name:
            raise ValueError(
                f"{ChatScene.ChatWithDbExecute.value} mode should chose db!"
            )
        with root_tracer.start_span(
            "ChatWithDbAutoExecute.get_connect", metadata={"db_name": self.db_name}
        ):
            self.database = CFG.local_db_manager.get_connector(self.db_name)

        self.top_k: int = 50
        self.api_call = ApiCall()

    @trace()
    async def generate_input_values(self) -> Dict:
        """
        generate input values
        """
        try:
            from dbgpt.rag.summary.db_summary_client import DBSummaryClient
        except ImportError:
            raise ValueError("Could not import DBSummaryClient. ")
        client = DBSummaryClient(system_app=CFG.SYSTEM_APP)
        table_infos = None
        try:
            with root_tracer.start_span("ChatWithDbAutoExecute.get_db_summary"):
                table_infos = await blocking_func_to_async(
                    self._executor,
                    client.get_db_summary,
                    self.db_name,
                    self.current_user_input if self.table_name is  None else self.table_name,
                    CFG.KNOWLEDGE_SEARCH_TOP_SIZE,
                )
                if self.table_name is not None :
                    table_infos = [d for d in table_infos if self.table_name in d]
                if len(table_infos) == 0:
                    raise Exception("not found table infos")
        except Exception as e:
            print("db summary find error!" + str(e))
        if not table_infos:
            print("db summary find error!" + str(e))
            # table_infos = await blocking_func_to_async(
            #     self._executor, self.database.table_simple_info
            # )
            
            
        logger.info(f"ChatWithDbAutoExecute -> table_infos {len(table_infos)}")

        input_values = {
            "db_name": self.db_name,
            "user_input": self.current_user_input,
            "top_k": str(self.top_k),
            "dialect": self.database.dialect,
            "table_info": table_infos,
            "display_type": self._generate_numbered_list(),
            "db_type": self.database.db_type,
            "table_name":envutils.getenv("CK_TABLE_NAME")
        }
        return input_values

    def stream_plugin_call(self, text):
        text = text.replace("\n", " ")
        print(f"stream_plugin_call:{text}")
        return self.api_call.display_sql_llmvis(text, self.database.run_to_df)

    def do_action(self, prompt_response):
        print(f"do_action:{prompt_response}")
        return self.database.run_to_df
