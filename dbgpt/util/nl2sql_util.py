import json
from decimal import Decimal
from typing import Dict

import requests

from dbgpt.util.nl2sql import nl2sql_card
from dbgpt.util.nl2sql import nl2sql_mapping
from datetime import datetime


def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {}
    # 数据分析助手机器人
    params = {
        'app_id': 'cli_a6a89ea1b851900d',
        'app_secret': 'O1cgHVtLtiShqynV6jUZYdvMQ4JduaTX'
    }
    resp = requests.post(url=url, headers=headers, params=params)
    print('\n飞书租户令牌返回结果：', resp.json())
    return resp.json()


def build_headers(token=None):
    if token is None:
        token = get_tenant_access_token()['tenant_access_token']
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json; charset=utf-8'
    }
    return headers


def is_time_format(v, format='%Y-%m-%d %H:%M:%S'):
    try:
        datetime.strptime(str(v).replace('T', ' '), format)
        return True
    except ValueError:
        return False


def send_table_card(data_json, receive_id, url, params):
    # 返回表格信息
    table_card = nl2sql_card.TableCard()
    table_card_template = table_card.template
    titles = []
    values = []
    title_set = set()
    for info in data_json:
        info1 = {}
        for k in info.keys():
            info1[k] = str(info[k])
            if k not in title_set:
                title_set.add(k)
                title = {"name": k, "display_name": k, "data_type": "text", "width": "auto"}
                titles.append(title)

        values.append(info1)

    if len(titles) > 0:
        table_card_template['elements'][0]['columns'] = titles
        table_card_template['elements'][0]['rows'] = values
        table_card_data = {
            "receive_id": receive_id,
            "msg_type": "interactive",
            "content": json.dumps(table_card_template)
        }

        resp = requests.request('POST', url=url, headers=build_headers(), params=params,
                                data=json.dumps(table_card_data))
        print('已经发送table卡片信息', resp.json())


def send_trend_chart_card(data_json, receive_id, url, params):
    # 返回趋势图信息
    mock_data = []
    # 判断是否有数字列
    flag = 0
    for info in data_json:
        for k in info.keys():
            v = info[k]
            if type(v) is int or type(v) is float:
                flag = 1
        break
    if flag == 0:
        print('无法生成趋势图')
        return
    mock_data_dicts = {}
    for info in data_json:
        if len(info) != 2:
            continue

        key = ''
        value = 0
        for k in info.keys():
            v = info[k]
            if type(v) is int or type(v) is float:
                value += Decimal(v)
            else:

                if type(v) is datetime or type(v) is str:
                    if is_time_format(v):
                        format = '%Y-%m-%d %H:%M:%S'
                        time = datetime.strptime(str(v).replace('T', ' '), format)
                        key = time

        if key not in mock_data_dicts.keys():
            mock_data_dicts[key] = float(value)
        else:
            mock_data_dicts[key] += float(value)

    for key in mock_data_dicts.keys():
        tmp = {'time': key, 'value': mock_data_dicts[key]}
        mock_data.append(tmp)

    mock_data = sorted(mock_data, key=lambda x: x['time'])
    for info in mock_data:
        # 默认按天处理趋势
        info['time'] = str(info['time'])[0:10]
    trend_chart_card = nl2sql_card.TrendChartCard(mock_data, "趋势图")
    template = trend_chart_card.get_template()
    if template:
        template_data = {
            "receive_id": receive_id,
            "msg_type": "interactive",
            "content": json.dumps(template)
        }
        resp = requests.request('POST', url=url, headers=build_headers(), params=params,
                                data=json.dumps(template_data))
        print('已经发送趋势图卡片信息', resp.json())


def send_pie_chart_card(data_json, receive_id, url, params):
    # 返回饼状图信息
    mock_data = []
    # 判断是否有数字列
    flag = 0
    for info in data_json:
        for k in info.keys():
            v = info[k]
            if type(v) is int or type(v) is float:
                flag = 1
        break
    if flag == 0:
        print('无法生成饼状图')
        return

    '''
    for info in data_json:
        for k in info.keys():
            v = info[k]
            if type(v) is int or type(v) is float:
                if float(v) < 0:
                    print('存在负数, 无法生成饼图')
                    return
    '''

    mock_data_dicts = {}
    for info in data_json:
        if len(info) != 2:
            continue
        key = ''
        value = 0
        for k in info.keys():
            v = info[k]
            if type(v) is int or type(v) is float:
                value += Decimal(v)
            else:
                key = v

        if value == 0:
            key = '其他'
        if key not in mock_data_dicts.keys():
            mock_data_dicts[key] = float(value)
        else:
            mock_data_dicts[key] += float(value)

    for key in mock_data_dicts.keys():
        mock_data.append({
            "type": key,
            "value": mock_data_dicts[key]
        })

    mock_data = sorted(mock_data, key=lambda x: x['value'])

    pie_chart_card = nl2sql_card.PieChartcard(mock_data, "饼状图")
    template = pie_chart_card.get_template()
    if template:
        template_data = {
            "receive_id": receive_id,
            "msg_type": "interactive",
            "content": json.dumps(template)
        }
        resp = requests.request('POST', url=url, headers=build_headers(), params=params,
                                data=json.dumps(template_data))
        print('已经发送饼状图卡片信息', resp.json())


def send_histogram_card(data_json, receive_id, url, params):
    # 返回直方图信息
    mock_data = []

    mock_data_dicts = {}
    flag = 0
    for info in data_json:

        for k in info.keys():
            v = info[k]
            if type(v) is int or type(v) is float:
                flag = 1
        break
    if flag == 0:
        print('无法生成直方图')
        return

    for info in data_json:
        if len(info) != 2:
            continue
        key = ''
        value = 0
        for k in info.keys():
            v = info[k]
            if type(v) is int or type(v) is float:
                value += Decimal(v)
            else:
                key = v
        if value == 0:
            key = '其他'
        if key not in mock_data_dicts.keys():
            mock_data_dicts[key] = float(value)
        else:
            mock_data_dicts[key] += float(value)

    for key in mock_data_dicts.keys():
        mock_data.append({
            "type": 'Autoc',
            "time":  key,
            "value": mock_data_dicts[key]
        })

    mock_data = sorted(mock_data, key=lambda x: x['value'])

    histogram_card = nl2sql_card.HistogramCard(mock_data, "分布图")
    template = histogram_card.get_template()
    if template:
        template_data = {
            "receive_id": receive_id,
            "msg_type": "interactive",
            "content": json.dumps(template)
        }
        resp = requests.request('POST', url=url, headers=build_headers(), params=params,
                                data=json.dumps(template_data))
        print('已经发送直方图卡片信息', resp.json())


def send_message(human_message: str, receive_id: str, content: Dict, receive_id_type: str = "email",
                 msg_type: str = "text"):
    url = 'https://open.feishu.cn/open-apis/im/v1/messages'
    params = {
        "receive_id_type": receive_id_type
    }
    # 解析数据
    res = ''
    sql_data = ''
    if '<chart-view content=' in content['text']:
        res = content['text'].split('<chart-view content="')[0]
        sql_data = content['text'].split('<chart-view content="')[1].replace('" />', '')

    # 不包含sql相关内容时，直接返回信息
    if len(res) == 0:
        res_data = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": json.dumps(content)
        }
        resp = requests.request('POST', url=url, headers=build_headers(), params=params, data=json.dumps(res_data))
        print('不包含sql相关内容时信息', resp.json())
    try:
        # 解析数据
        sql_data_json = json.loads(sql_data)
        data_json = sql_data_json['data']
        sql = sql_data_json['sql']
        # 包含sql相关内容时，返回信息
        res_data = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": json.dumps({'text': res + ' sql: ' + sql}),
        }
        resp = requests.request('POST', url=url, headers=build_headers(), params=params, data=json.dumps(res_data))
        print('包含sql相关内容时信息', resp.json())
        # 字段变换
        data_base_filed = nl2sql_mapping.DataBaseFiled()
        data_json1 = []
        for data in data_json:
            data1 = {}
            for key in data.keys():
                if key in data_base_filed.dataBaseFiledDict.keys():
                    key1 = data_base_filed.dataBaseFiledDict[key]
                    data1[key1] = data[key]
                else:
                    data1[key] = data[key]
            data_json1.append(data1)

        # 返回表格信息
        send_table_card(data_json1, receive_id, url, params)
        # 返回图表信息

        if '趋势' in human_message or '折线' in human_message:
            send_trend_chart_card(data_json1, receive_id, url, params)

        send = 0
        if '饼图' in human_message or '饼状'in human_message:
            send_pie_chart_card(data_json1, receive_id, url, params)
            send = 1
        if '柱状' in human_message or '直方' in human_message:
            send_histogram_card(data_json1, receive_id, url, params)
            send = 1
        if send == 0 and '分布' in human_message:
            send_histogram_card(data_json1, receive_id, url, params)

    except Exception as e:
        print('查数据解析错误')
        raise e
