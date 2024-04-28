import json

import requests


#  趋势图、折线图
class TrendChartCard:

    def __init__(self, mock_data, title):
        self.mock_data = mock_data
        self.title = title

    def isValid(self):
        if not self.title or len(self.title) == 0:
            self.title = '趋势图'
        if not self.mock_data or len(self.mock_data) == 0:
            return False
        keys = self.mock_data[0].keys()
        if 'time' not in keys or 'value' not in keys:
            return False

        return True

    # case
    """
    mock_data = [
        {
            "time": "2:00",
            "value": 8
        },
        {
            "time": "4:00",
            "value": 9
        },
        {
            "time": "18:00",
            "value": 15
        }
    ]
    """

    def get_template(self):
        if not self.isValid():
            return None
        template = {
            "elements": [
                {
                    "tag": "chart",
                    "chart_spec": {
                        "type": "line",
                        "title": {
                            "text": ""
                        },
                        "data": {
                            "values": self.mock_data  # 此处传入数据。
                        },
                        "xField": "time",
                        "yField": "value"
                    }
                }
            ],
            "header": {
                "template": "purple",
                "title": {"content": self.title, "tag": "plain_text"}
            }
        }
        return template


# 直方图、柱状图
class HistogramCard:
    def __init__(self, mock_data, title):
        self.mock_data = mock_data
        self.title = title

    def isValid(self):
        if not self.title or len(self.title) == 0:
            self.title = '柱状图'
        if not self.mock_data or len(self.mock_data) == 0:
            return False
        keys = self.mock_data[0].keys()
        if 'type' not in keys or 'time' not in keys or 'value' not in keys:
            return False

        return True

    # case
    """
    mock_data = [
        {"type": "Autoc", "time": "1930", "value": 129},
        {"type": "Autoc", "time": "1940", "value": 133},
        {"type": "Autoc", "time": "1950", "value": 130},
        {"type": "Autoc", "time": "1960", "value": 126},
        {"type": "Democ", "time": "1930", "value": 22},
        {"type": "Democ", "time": "1940", "value": 13},
        {"type": "Democ", "time": "1950", "value": 25}
    ]
    """

    def get_template(self):
        if not self.isValid():
            return None
        template = {
            "elements": [
                {
                    "tag": "chart",
                    "chart_spec": {
                        "type": "bar",
                        "title": {
                            "text": ""
                        },
                        "data": {
                            "values": self.mock_data  # 此处传入数据。
                        },
                        "xField": ["time", "type"],
                        "yField": "value",
                        "seriesField": "type",
                        "legends": {
                            "visible": True,
                            "orient": "bottom"
                        }
                    }
                }
            ],
            "header": {
                "template": "purple",
                "title": {"content": self.title, "tag": "plain_text"}
            }
        }
        return template


# 饼状图
class PieChartcard:
    def __init__(self, mock_data, title):
        self.mock_data = mock_data
        self.title = title

    def isValid(self):
        if not self.title or len(self.title) == 0:
            self.title = '饼状图'
        if not self.mock_data or len(self.mock_data) == 0:
            return False
        keys = self.mock_data[0].keys()
        if 'type' not in keys or 'value' not in keys:
            return False

        return True

    # case
    """
    mock_data = [
        {
            "type": "S1",
            "value": "340"
        },
        {
            "type": "S2",
            "value": "170"
        },
        {
            "type": "S3",
            "value": "150"
        },
        {
            "type": "S4",
            "value": "120"
        },
        {
            "type": "S5",
            "value": "100"
        }
    ]
    """

    def get_template(self):
        if not self.isValid():
            return None
        template = {
            "elements": [
                {
                    "tag": "chart",
                    "aspect_ratio": "4:3",
                    "chart_spec": {
                        "type": "pie",
                        "title": {
                            "text": self.title
                        },
                        "data": {
                            "values": self.mock_data  # 此处传入数据。
                        },
                        "valueField": "value",
                        "categoryField": "type",
                        "outerRadius": 0.9,
                        "legends": {
                            "visible": True,
                            "orient": "right"
                        },
                        "padding": {
                            "left": 10,
                            "top": 10,
                            "bottom": 5,
                            "right": 0
                        },
                        "label": {
                            "visible": True
                        }
                    }
                }
            ]
        }
        return template


class CompositeCard:
    def __init__(self, mock_data1, mock_data2, title):

        self.mock_data1 = mock_data1
        self.mock_data2 = mock_data2
        self.title = title

    def isValid(self):
        if not self.title or len(self.title) == 0:
            self.title = '组合图'
        if not self.mock_data1 or len(self.mock_data1) == 0 or not self.mock_data2 or len(self.mock_data2) == 0:
            return False
        keys1 = self.mock_data1[0].keys()
        keys2 = self.mock_data2[0].keys()
        if 'x' not in keys1 or 'y' not in keys1 or 'type' not in keys1:
            return False
        if 'x' not in keys2 or 'y' not in keys2 or 'type' not in keys2:
            return False
        return True

    # case
    """
    mock_data1 = [
        {"x": "周一", "type": "早餐", "y": 15},
        {"x": "周一", "type": "午餐", "y": 25},
        {"x": "周二", "type": "早餐", "y": 12},
        {"x": "周二", "type": "午餐", "y": 30},
        {"x": "周三", "type": "早餐", "y": 15},
        {"x": "周三", "type": "午餐", "y": 24},
        {"x": "周四", "type": "早餐", "y": 10},
        {"x": "周四", "type": "午餐", "y": 25},
        {"x": "周五", "type": "早餐", "y": 13},
        {"x": "周五", "type": "午餐", "y": 20},
        {"x": "周六", "type": "早餐", "y": 10},
        {"x": "周六", "type": "午餐", "y": 22},
        {"x": "周日", "type": "早餐", "y": 12},
        {"x": "周日", "type": "午餐", "y": 19}
    ]
    mock_data2 = [
        {"x": "周一", "type": "饮料", "y": 22},
        {"x": "周二", "type": "饮料", "y": 43},
        {"x": "周三", "type": "饮料", "y": 33},
        {"x": "周四", "type": "饮料", "y": 22},
        {"x": "周五", "type": "饮料", "y": 10},
        {"x": "周六", "type": "饮料", "y": 30},
        {"x": "周日", "type": "饮料", "y": 50}
    ]
    """

    def get_template(self):
        if not self.isValid():
            return None
        template = {
            "elements": [
                {
                    "tag": "chart",
                    "chart_spec": {
                        "type": "common",
                        "title": {
                            "text": ""
                        },
                        "data": [
                            {
                                "values": self.mock_data1  # 此处传入数据。
                            },
                            {
                                "values": self.mock_data2  # 此处传入数据。
                            }
                        ],
                        "series": [
                            {
                                "type": "bar",
                                "dataIndex": 0,
                                "label":
                                    {
                                        "visible": True
                                    },
                                "seriesField": "type",
                                "xField": ["x", "type"],
                                "yField": "y"
                            },
                            {
                                "type": "line",
                                "dataIndex": 1,
                                "label": {
                                    "visible": True
                                },
                                "seriesField": "type",
                                "xField": "x",
                                "yField": "y"
                            }
                        ],
                        "axes": [
                            {
                                "orient": "bottom"
                            },
                            {
                                "orient": "left"
                            }
                        ],
                        "legends": {
                            "visible": True,
                            "orient": "bottom"
                        }
                    }
                }
            ],
            "header": {
                "template": "purple",
                "title": {"content": self.title, "tag": "plain_text"}
            }
        }
        return template


class TableCard:
    template = {
        "header": {
            "template": "blue",
            "title": {
                "content": "结果展示",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "table",
                "page_size": 5,
                "row_height": "middle",
                "header_style": {
                    "bold": True,
                    "background_style": "grey",
                    "lines": 1,
                    "text_size": "heading",
                    "text_align": "center"
                },
                "columns": [
                    # {
                    #     "name": "customer_name",
                    #     "display_name": "客户名称",
                    #     "data_type": "text"
                    # },
                    # {
                    #     "name": "customer_scale",
                    #     "display_name": "客户规模",
                    #     "data_type": "options",
                    #     "width": "90px"
                    # },
                    # {
                    #     "name": "customer_arr",
                    #     "display_name": "ARR(万元)",
                    #     "data_type": "number",
                    #     "format": {
                    #         "symbol": "¥",
                    #         "precision": 2
                    #     },
                    #     "width": "120px"
                    # },
                    # {
                    #     "name": "customer_year",
                    #     "display_name": "签约年限",
                    #     "data_type": "text"
                    # }
                ],
                "rows": [
                    # {
                    #     "customer_name": "飞书消息卡片是飞书中的一种功能，它允许用户通过机器人或应用以结构化（JSON）的方式发送和接收消息。",
                    #     "customer_scale": [
                    #         {
                    #             "text": "S2",
                    #             "color": "green"
                    #         }
                    #     ],
                    #     "customer_arr": 26.57774928467545,
                    #     "customer_year": "2年"
                    # }
                ]
            }
        ]
    }


if __name__ == '__main__':
    mock_data = [
        {
            "time": "2:00",
            "value": 8
        },
        {
            "time": "4:00",
            "value": 9
        },
        {
            "time": "18:00",
            "value": 15
        }
    ]
    trendChartCard = TrendChartCard(mock_data, "卡片测试")
    template = trendChartCard.get_template()
    print(template)
