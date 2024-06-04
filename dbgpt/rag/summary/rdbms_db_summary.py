"""Summary for rdbms database."""
import json
import logging
import re
from typing import TYPE_CHECKING, List, Optional

from dbgpt._private.config import Config
from dbgpt.datasource import BaseConnector
from dbgpt.rag.summary.db_summary import DBSummary
from dbgpt.util import envutils
from dbgpt.util.azure_util import create_azure_llm
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks import get_openai_callback







if TYPE_CHECKING:
    from dbgpt.datasource.manages import ConnectorManager

CFG = Config()

logger = logging.getLogger(__name__)

prompt_template = """
你是一名数据分析师，可以帮助总结SQL表格。 根据给定的上下文总结以下表格。
 
===表格结构信息
{table_schema}

===回复指南
1. 你应当只根据提供的信息撰写总结。
2. 不要使用任何形容词来描述表格。例如，表格的重要性、其全面性或其是否关键，或谁可能使用它。例如，你可以说表格包含某些类型的数据，但不能说表格包含“大量”的数据，或说它是“全面的”。
3. 不要提及示例查询。只客观地谈论表格包含的数据类型及其可能的用途。
4. 请全部写出来每一列对应的可能的值。
"""
# 5. 请同时多包含一些表格的潜在使用案例，例如该表格可以回答哪些类型的问题，可以进行哪些类型的分析等。

TABLE_SUMMARY_PROMPT = PromptTemplate.from_template(prompt_template)

class RdbmsSummary(DBSummary):
    """Get rdbms db table summary template.

    Summary example:
        table_name(column1(column1 comment),column2(column2 comment),
        column3(column3 comment) and index keys, and table comment is {table_comment})
    """

    def __init__(
        self, name: str, type: str, manager: Optional["ConnectorManager"] = None
    ):
        """Create a new RdbmsSummary."""
        self.name = name
        self.type = type
        self.summary_template = "{table_name}({columns})"
        self.tables = {}
        # self.tables_info = []
        # self.vector_tables_info = []

        # TODO: Don't use the global variable.
        db_manager = manager or CFG.local_db_manager
        if not db_manager:
            raise ValueError("Local db manage is not initialized.")
        self.db = db_manager.get_connector(name)

        self.metadata = """user info :{users}, grant info:{grant}, charset:{charset},
        collation:{collation}""".format(
            users=self.db.get_users(),
            grant=self.db.get_grants(),
            charset=self.db.get_charset(),
            collation=self.db.get_collation(),
        )
            
        # tables = [tb for tb in self.db.get_table_names() if tb in embedding_tables]
        # self.table_info_summaries = [
        #     self.get_table_summary(table_name) for table_name in tables
        # ]
        

    def get_table_summary(self, table_name):
        """Get table summary for table.

        example:
            table_name(column1(column1 comment),column2(column2 comment),
            column3(column3 comment) and index keys, and table comment: {table_comment})
        """
        return _parse_table_summary(self.db, self.summary_template, table_name)

    def table_summaries(self):
        """Get table summaries."""
        return self.table_info_summaries


def _parse_db_summary(
    conn: BaseConnector, summary_template: str = "{table_name}({columns})"
) -> List[str]:
    """Get db summary for database.

    Args:
        conn (BaseConnector): database connection
        summary_template (str): summary template
    """
    # tables = conn.get_table_names()
    
    try:
        # comment: 
        embedding_tables = json.loads(envutils.getenv("EMBEDDING_TABLES_CONIFG"))
    except Exception as e:
        embedding_tables = []
        logger.info(f"ENV: EMBEDDING_TABLES_CONIFG parse error ")
        
    tables = [tb for tb in conn.get_table_names() if tb in embedding_tables]
    
    table_info_summaries = [
        _parse_table_summary(conn, summary_template, table_name)
        for table_name in tables
    ]
    return table_info_summaries


def _parse_table_summary(
    conn: BaseConnector, summary_template: str, table_name: str
) -> str:
    """Get table summary for table.

    Args:
        conn (BaseConnector): database connection
        summary_template (str): summary template
        table_name (str): table name

    Examples:
        table_name(column1(column1 comment),column2(column2 comment),
        column3(column3 comment) and index keys, and table comment: {table_comment})
    """
 
    
    # add field examples
    # fields_examples = [
    #     # '\nHere is a series of fields with their possible options, including but not limited to these: '
    # ]
    fields_examples = ''
    columns = []
    for column in conn.get_columns(table_name):
        if column.get("comment"):
            columns.append(f"{column['name']} ({column.get('comment')})")
        else:
            columns.append(f"{column['name']}")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
        if column.get('sample'):
            fields_examples += f"\n{column['name']}: {column.get('sample')}"
    # for column in conn.get_columns(table_name):
    #     if column.get("comment"):
    #         col = f"{column['name']} ({column.get('comment')}"
    #         if column.get('sample'):
    #             col += f": {column.get('sample')})"
    #         else:
    #             col += ")"
    #         columns.append(col)
    #     else:
    #         col = f"{column['name']}"
    #         if column.get('sample'):
    #             col += f"({column.get('sample')})"
    #         columns.append(col)
            

    column_str = ", ".join(columns)
    # Obtain index information
    index_keys = []
    raw_indexes = conn.get_indexes(table_name)
    for index in raw_indexes:
        if isinstance(index, tuple):  # Process tuple type index information
            index_name, index_creation_command = index
            # Extract column names using re
            matched_columns = re.findall(r"\(([^)]+)\)", index_creation_command)
            if matched_columns:
                key_str = ", ".join(matched_columns)
                index_keys.append(f"{index_name}(`{key_str}`) ")
        else:
            key_str = ", ".join(index["column_names"])
            index_keys.append(f"{index['name']}(`{key_str}`) ")
    table_str = summary_template.format(table_name=table_name, columns=column_str)
    if len(index_keys) > 0:
        index_key_str = ", ".join(index_keys)
        table_str += f", and index keys: {index_key_str}"
    try:
        comment = conn.get_table_comment(table_name)
    except Exception:
        comment = dict(text=None)
    if comment.get("text"):
        table_str += f", and table comment: {comment.get('text')}"
    # if len(fields_examples) > 1:
    #     table_str += fields_examples
        # table_str += '\n'.join(fields_examples)
        
        
       
    # 新增使用GPT生产数据库的总结
    """Generate table schema prompt. The format will be like:
    Table Name: [Name_of_table_1]
    Description: [Brief_general_description_of_Table_1]
    Columns:
    - Column Name: [Column1_name]
        Data Type: [Column1_data_type]
        Description: [Brief_description_of_the_column1_purpose]
    - Column Name: [Column2_name]
        Data Type: [Column2_data_type]
        Description: [Brief_description_of_the_column2_purpose]
        Data Element: [Data_element_name]
    """
    
    _prompt_table_schema = [
        f"""
        表格名称: [{table_name}]
        """
    ]
    if comment.get("text"):
        _prompt_table_schema.append(f"表格描述: [{comment.get('text')}]")
    
    _prompt_table_schema.append("所有列信息:")
    
    for column in conn.get_columns(table_name):
        
        field_schema = [
            f"- 列名称: [{column['name']}]",
            f"    数据类型: [{column['type']}]"
        ]
        if column.get("comment"):
            field_schema.append(f"    描述: [{column['comment']}]")
        if column.get("sample"):
            field_schema.append(f"    可能的值: [{column['sample']}]")
        
        _prompt_table_schema.append("\n".join(field_schema))   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    
    
    prompt = TABLE_SUMMARY_PROMPT.format(table_schema='\n'.join(_prompt_table_schema))
    
    
    llm = create_azure_llm()
    res = llm.invoke([HumanMessage(content=prompt)])
    
    print(res)
    return res.content
    return table_str
