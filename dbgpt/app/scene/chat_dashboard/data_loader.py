import logging
from decimal import Decimal
from typing import List

from dbgpt._private.config import Config
from dbgpt.app.scene.chat_dashboard.data_preparation.report_schma import ValueItem
from datetime import date, time, datetime

CFG = Config()
logger = logging.getLogger(__name__)


class DashboardDataLoader:
    def get_sql_value(self, db_conn, chart_sql: str):
        return db_conn.query_ex(chart_sql)

    def get_chart_values_by_conn(self, db_conn, chart_sql: str, chart_type:str = None):
        field_names, datas = db_conn.query_ex(chart_sql)
        return self.get_chart_values_by_data(field_names, datas, chart_sql,chart_type)

    def get_chart_values_by_data(self, field_names, datas, chart_sql: str, chart_type:str = None):
        logger.info(f"get_chart_values_by_conn:{chart_sql}")
        # try:
        values: List[ValueItem] = []
        data_map = {}

        data_map.update(
            {
                f"{field_name}": [row[index] for row in datas]
                for index, field_name in enumerate(field_names)
            }
        )
        # to Check Whether there are data in it
        if len(datas) != 0:
            # find the first string column
            str_index = next(
                (
                    index
                    for index, value in enumerate(datas[0])
                    if isinstance(value, str)
                ),
                None,
            )
            if str_index is not None and type(datas[0][str_index]) == str:
                tempFieldName = field_names[:str_index]
                tempFieldName.extend(field_names[str_index + 1 :])
                for field_name in tempFieldName:
                    for data in datas:
                        # None Data won't be ok for the chart
                        if not any(item is None for item in data):
                            value_item = ValueItem(
                                name=data[str_index],
                                type=field_name,
                                value=(data[field_names.index(field_name)]),
                            )
                            values.append(value_item)
                        else:
                            value_item = ValueItem(
                                name=data[str_index],
                                type=field_name,
                                value=0,
                            )
                            values.append(value_item)
            else:
                    # comment: 
                    if chart_type == "Table":
                        for di, d in enumerate(datas):  # looping through row
                            for fi, field_name in enumerate(field_names):  # looping through row
                            # comment: 
                                # comment: 
                                value_item = ValueItem(
                                    type=field_name,
                                    value=str(d[fi]),
                                    name=field_name
                                )
                                values.append(value_item)
                            # end for
                        # end for
                    else:    
                        for idx, d in enumerate(datas):  # looping through row
                            value_item = ValueItem(
                                name=str(get_tuple_value(d, 0) or '0'),
                                value=(get_tuple_value(d, 1) or '0'),
                                type=str(get_tuple_value(d, 2) or f"{field_names[0]}_${idx}")
                            )
                            values.append(value_item)
                # end for
            # elif check_row_numeric(datas[0]):
            #     str_index = 1
                
            #     # result = [sum(values) for values in zip(*datas)]
            #     result = [50,100]
            #     # result = [sum(value for value in values if not self.is_time_type(value)) for values in zip(*datas)]
            #     for index, field_name in enumerate(field_names):
            #         value_item = ValueItem(
            #             name=field_name,
            #             type=f"{field_name}_count",
            #             value=str(result[index]),
            #         )
                    # values.append(value_item)
            # elif check_row_has_date(datas[0]) :
            #     for index, d in enumerate(datas):
            #         # for inner_idx,d_item in enumerate(d) :
            #         value_item = ValueItem(
            #             name=str(d[0]),
            #             type=f"{'-'.join(field_names)}_count",
            #             value=str(d[1]),
            #         )
            #         values.append(value_item)
                
            return field_names, values
        else:
            return field_names, [
                ValueItem(name=f"{field_name}", type=f"{field_name}", value="0")
                for index, field_name in enumerate(field_names)
            ]

    def get_chart_values_by_db(self, db_name: str, chart_sql: str):
        logger.info(f"get_chart_values_by_db:{db_name},{chart_sql}")
        db_conn = CFG.local_db_manager.get_connector(db_name)
        return self.get_chart_values_by_conn(db_conn, chart_sql)


    
    
    
    
def is_time_type(obj):
    return isinstance(obj, (date, time, datetime))



def check_row_numeric(row):
    # 遍历三元组的所有元素
    for item in row:
        # 如果元素不是数字类型，则返回False
        if not isinstance(item, (int, float)):
            return False
    # 如果所有元素都是数字类型，则返回True
    return True

def check_row_has_date(row):
    # 遍历三元组的所有元素
    for item in row:
        # 如果元素不是数字类型，则返回False
        if is_time_type(item):
            return True
    # 如果所有元素都是数字类型，则返回True
    return False

def get_tuple_value(tpl, index):
    if 0 <= index < len(tpl):
        return tpl[index]
    else:
        return None 