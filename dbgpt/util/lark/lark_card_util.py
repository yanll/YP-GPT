from typing import Dict

from dbgpt.util.lark import lark_message_util


def send_message_with_bingo(receive_id: str, template_variable: Dict):
    """包含点赞、新会话功能的消息卡片"""
    card = create_card_content_by_template("AAqkIdjGltfge", "1.0.14", template_variable)
    return lark_message_util.send_message(
        receive_id=receive_id,
        receive_id_type="open_id",
        content=card,
        msg_type="interactive"
    )


def send_message_with_welcome(receive_id: str, template_variable: Dict):
    """欢迎卡片"""
    card = create_card_content_by_template(
        template_id="AAqkIeluuBZF2",
        template_version_name="1.0.13",
        template_variable=template_variable
    )
    return lark_message_util.send_message(
        receive_id=receive_id,
        receive_id_type="open_id",
        content=card,
        msg_type="interactive"
    )


def create_card_content_by_template(template_id: str, template_version_name: str, template_variable: Dict):
    """"""
    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def card_options_to_input_field_description(options: list) -> str:
    """将卡片选项转换为参数接收字段中的选项描述"""
    options_str = "共" + str(len(options)) + "个选项："
    for option in options:
        options_str += option['text'] + "、"
    rs = options_str[:-1]
    print("卡片选项转换结果：", rs)
    return rs


def get_action_index_by_text_from_options(text, options: list) -> int:
    """根据文本选索引，默认返回第一个"""
    for option in options:
        if option["text"] == text:
            return option["action_index"]
    return 1


def get_action_index_by_value_from_options(value, options: list) -> int:
    """根据值选索引，默认返回第一个"""
    for option in options:
        if option["action_value"] == value:
            return option["action_index"]
    return 1


def get_value_by_text_from_options(text, options: list):
    for option in options:
        if option["text"] == text:
            return option["action_value"]
    return ""


def get_text_by_value_from_options(value, options: list):
    for option in options:
        if option["action_value"] == value:
            return option["text"]
    return ""


def card_options_for_requirement_emergency_level() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "0", "text": "非常紧急"},
        {"action_index": 2, "action_value": "1", "text": "紧急"},
        {"action_index": 3, "action_value": "2", "text": "高"},
        {"action_index": 4, "action_value": "99", "text": "中"},
        {"action_index": 5, "action_value": "1sdyyo6lh", "text": "低"}
        # 1sdyyo6lh
    ]
    return options


def card_options_for_requirement_industry_line() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "662db530cde8ed174622a08d", "text": "航旅行业线"},
        {"action_index": 2, "action_value": "662db56afe2c0b51b33668eb", "text": "大零售行业线"},
        {"action_index": 3, "action_value": "662db596fe2c0b51b33668ec", "text": "线上线下一体化"},
        {"action_index": 4, "action_value": "662db5b688aa18a943e64644", "text": "老板管账"},
        {"action_index": 5, "action_value": "662db5c3a55775e2c9c83bf9", "text": "金融行业线"}
    ]
    return options


def card_options_for_customer_role() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "标准商户", "text": "标准商户"},
        {"action_index": 2, "action_value": "服务商", "text": "服务商"},
        {"action_index": 3, "action_value": "平台商", "text": "平台商"},
        {"action_index": 4, "action_value": "平台入驻客户", "text": "平台入驻客户"},
        {"action_index": 5, "action_value": "分账客户", "text": "分账客户"},
        {"action_index": 6, "action_value": "代理商", "text": "代理商"},
        {"action_index": 7, "action_value": "分账接受方", "text": "分账接受方"},
    ]
    return options


def card_options_for_industry_line() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "Web3.0行业线", "text": "Web3.0行业线"},
        {"action_index": 2, "action_value": "金融行业线", "text": "金融行业线"},
        {"action_index": 3, "action_value": "大零售行业线", "text": "大零售行业线"},
        {"action_index": 4, "action_value": "跨境行业线", "text": "跨境行业线"},
        {"action_index": 5, "action_value": "外综服行业线", "text": "外综服行业线"},
        {"action_index": 6, "action_value": "大出行项目组", "text": "大出行项目组"},
        {"action_index": 7, "action_value": "政务行业线", "text": "政务行业线"},
        {"action_index": 8, "action_value": "航旅事业部", "text": "航旅事业部"},
    ]
    return options


class card_options_for_business_type:
    """值必须和飞书项目一致"""

    @staticmethod
    def Finance():
        options = [
            {"action_index": 1, "action_value": "银行", "text": "银行"},
            {"action_index": 2, "action_value": "车抵房抵", "text": "车抵房抵"},
            {"action_index": 3, "action_value": "融资担保", "text": "融资担保"},
            {"action_index": 4, "action_value": "逃废债", "text": "逃废债"},
            {"action_index": 5, "action_value": "消费贷", "text": "消费贷"},
            {"action_index": 6, "action_value": "信托", "text": "信托"},
            {"action_index": 7, "action_value": "助贷平台", "text": "助贷平台"},
            {"action_index": 8, "action_value": "会员权益", "text": "会员权益"},
            {"action_index": 9, "action_value": "消费金融", "text": "消费金融"},
            {"action_index": 10, "action_value": "小贷/网贷", "text": "小贷/网贷"},
            {"action_index": 11, "action_value": "其他", "text": "其他"},
        ]
        return options

    @staticmethod
    def CrossBorder():
        options = [
            {"action_index": 1, "action_value": "货物贸易", "text": "货物贸易"},
            {"action_index": 2, "action_value": "国际运输", "text": "国际运输"},
            {"action_index": 3, "action_value": "航空机票", "text": "航空机票"},
            {"action_index": 4, "action_value": "酒店住宿", "text": "酒店住宿"},
            {"action_index": 5, "action_value": "PSP", "text": "PSP"},
            {"action_index": 6, "action_value": "其他直签客户", "text": "其他直签客户"},
            {"action_index": 7, "action_value": "其他", "text": "其他"},
        ]
        return options

    @staticmethod
    def Retail():
        options = [
            {"action_index": 1, "action_value": "加油站/能源", "text": "加油站/能源"},
            {"action_index": 2, "action_value": "供应链平台", "text": "供应链平台"},
            {"action_index": 3, "action_value": "撮合型平台(电商)", "text": "撮合型平台(电商)"},
            {"action_index": 4, "action_value": "品牌连锁直/分销", "text": "品牌连锁直/分销"},
            {"action_index": 5, "action_value": "二手市场买卖", "text": "二手市场买卖"},
            {"action_index": 6, "action_value": "人力资源劳务发放", "text": "人力资源劳务发放"},
            {"action_index": 7, "action_value": "其他", "text": "其他"},
            {"action_index": 8, "action_value": "税务科技", "text": "税务科技"},
        ]
        return options

    @staticmethod
    def Government():
        options = [
            {"action_index": 1, "action_value": "公立院校", "text": "加油站/能源"},
            {"action_index": 2, "action_value": "民办学院", "text": "供应链平台"},
            {"action_index": 3, "action_value": "私立学校", "text": "撮合型平台(电商)"},
            {"action_index": 4, "action_value": "事业单位", "text": "品牌连锁直/分销"},
            {"action_index": 5, "action_value": "政府机构", "text": "二手市场买卖"},
            {"action_index": 6, "action_value": "协会性质", "text": "人力资源劳务发放"},
            {"action_index": 7, "action_value": "基金会及下属关联企业项目(有函件或批文证明关联关系)",
             "text": "税务科技"},
            {"action_index": 8, "action_value": "其他", "text": "其他"},
        ]
        return options

    class AirTravel:
        @staticmethod
        def Category_I():
            data = {
                '出行': ['出行平台商及服务商', '共享出行', '火车票', '汽车票', '出行周边服务商'],
                '通信': ['通信'],
                '酒店住宿': ['单体酒店', '民俗公寓等集团', '酒店集团', '系统商', '酒店周边', '酒店代理/包房商']
            }
            """值必须和飞书项目一致"""
            options = []
            for index, aspect in enumerate(data):
                for sub_aspect in data[aspect]:
                    option = {"action_index": index + 1, "action_value": f"{aspect}:{sub_aspect}",
                              "text": f"{aspect}:{sub_aspect}"}
                    options.append(option)
            return options

        @staticmethod
        def Category_II():
            data = {
                '旅游': ['文旅集团/综合体', '旅行社', '景区', '周边游/本地生活', '旅游周边'],
                '航空': ['航司', '票代', 'TMC', 'OTA', '其他航空业务', '票代TMC']
            }
            """值必须和飞书项目一致"""
            options = []
            for index, aspect in enumerate(data):
                for sub_aspect in data[aspect]:
                    option = {"action_index": index + 1, "action_value": f"{aspect}:{sub_aspect}",
                              "text": f"{aspect}:{sub_aspect}"}
                    options.append(option)
            return options

        @staticmethod
        def description():
            return "所属行业的分类，共有两个选项：第一类、第二类。第一类中包括出行、通信、酒店住宿。第二类包括旅游、航空。"


def card_options_for_customer_source() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "电话营销", "text": "电话营销"},
        {"action_index": 2, "action_value": "主动来电", "text": "主动来电"},
        {"action_index": 3, "action_value": "客户介绍", "text": "客户介绍"},
        {"action_index": 4, "action_value": "朋友介绍", "text": "朋友介绍"},
        {"action_index": 5, "action_value": "独立开发", "text": "独立开发"},
        {"action_index": 6, "action_value": "网络搜索", "text": "网络搜索"},
        {"action_index": 7, "action_value": "广告杂志", "text": "广告杂志"},
        {"action_index": 8, "action_value": "展会促销", "text": "展会促销"},
        {"action_index": 9, "action_value": "其他途径", "text": "其他途径"},
    ]
    return options


def card_options_for_customer_importance() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "一般商户", "text": "一般商户"},
        {"action_index": 2, "action_value": "重要商户", "text": "重要商户"},
        {"action_index": 3, "action_value": "KA商户", "text": "KA商户"},
    ]
    return options


def card_options_for_zw_client_assets() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "是", "text": "是"},
        {"action_index": 2, "action_value": "否", "text": "否"},
    ]
    return options


def card_options_for_zw_business_type() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "支付", "text": "支付"},
        {"action_index": 2, "action_value": "支付+票据", "text": "支付+票据"},
        {"action_index": 3, "action_value": "票据", "text": "票据"},
        {"action_index": 4, "action_value": "系统服务", "text": "系统服务"},
        {"action_index": 5, "action_value": "其他", "text": "其他"},
    ]
    return options


def card_options_for_zw_province() -> list:
    data = [
        "北京市",
        "天津市", "上海市", "河北省", "山西省", "辽宁省", "吉林省", "黑龙江省", "江苏省", "浙江省", "安徽省", "福建省",
        "江西省", "山东省", "河南省", "湖北省", "湖南省", "广东省", "海南省", "四川省", "贵州省", "云南省", "陕西省",
        "甘肃省", "青海省", "台湾省", "内蒙古自治区", "广西壮族自治区", "西藏自治区",
        "宁夏回族自治区", "新疆维吾尔自治区", "香港特别行政区", "澳门特别行政区",

    ]
    """值必须和飞书项目一致"""
    options = []
    for index, option in enumerate(data):
        options.append({"action_index": index + 1, "action_value": option, "text": option})
    return options


def card_options_for_customer_size() -> list:
    data = [
        "10人以内", "10-20人", "21人-50人", "51人-200人", "201人-500人", "500人以上"
    ]
    """值必须和飞书项目一致"""
    options = []
    for index, option in enumerate(data):
        options.append({"action_index": index + 1, "action_value": option, "text": option})
    return options


def card_options_for_important_step() -> list:
    data = [
        "潜在客户", "确认合作意向", "方案阶段", "洽谈签约", "提单阶段"
    ]
    """值必须和飞书项目一致"""
    options = []
    for index, option in enumerate(data):
        options.append({"action_index": index + 1, "action_value": option, "text": option})
    return options


def card_options_for_purchasing_channels() -> list:
    data = {
        '机票': ['无', '携程', '去哪儿', '同程', '美团', '飞猪', '航旅纵横', '智行', '航司直采', '其他渠道'],
        '旅游': ['无', '携程', '去哪儿', '同程', '美团', '途牛', '智行', '喜玩', '其他渠道'],
        '酒店': ['无', '携程', '去哪儿', '同程', '美团', '途牛', '艺龙', '喜玩', '汇智酒店B2B', '绿云酒店库存',
                 '龙腾捷旅', 'Agoda', 'Booking', 'Taap-Expedia', 'Webbeds', 'Hotelbeds', '其他渠道'],
    }
    """值必须和飞书项目一致"""
    options = []
    for index, aspect in enumerate(data):
        for sub_aspect in data[aspect]:
            option = {"action_index": index + 1, "action_value": f"{aspect}:{sub_aspect}",
                      "text": f"{aspect}:{sub_aspect}"}
            options.append(option)
    return options


def card_options_for_payment_scene() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "线上", "text": "线上"},
        {"action_index": 2, "action_value": "线下", "text": "线下"},
    ]
    return options

def card_options_for_sales_channel() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "无", "text": "无"},
        {"action_index": 2, "action_value": "抖音APP", "text": "抖音APP"},
        {"action_index": 3, "action_value": "微信小程序", "text": "微信小程序"},
        {"action_index": 4, "action_value": "微信公众号", "text": "微信公众号"},
        {"action_index": 5, "action_value": "支付宝小程序", "text": "支付宝小程序"},
        {"action_index": 6, "action_value": "支付宝生活号", "text": "支付宝生活号"},
        {"action_index": 7, "action_value": "小红书APP", "text": "小红书APP"},
        {"action_index": 8, "action_value": "自营官网", "text": "自营官网"},
        {"action_index": 9, "action_value": "APP", "text": "APP"},
        {"action_index": 10, "action_value": "其他", "text": "其他"},
    ]
    return options


def card_options_for_zw_customer_level() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "中央", "text": "中央"},
        {"action_index": 2, "action_value": "省级", "text": "省级"},
        {"action_index": 3, "action_value": "地市", "text": "地市"},
        {"action_index": 4, "action_value": "其他", "text": "其他"},
    ]
    return options


def card_options_for_product_type() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "APP", "text": "APP"},
        {"action_index": 2, "action_value": "小程序", "text": "小程序"},
        {"action_index": 3, "action_value": "公众号", "text": "公众号"},
        {"action_index": 4, "action_value": "生活号", "text": "生活号"},
        {"action_index": 5, "action_value": "网站", "text": "网站"}
    ]
    return options


def card_options_for_visit_methods() -> list:
    """拜访形式"""
    options = [
        {"action_index": 1, "action_value": "电话/微信拜访", "text": "电话/微信拜访"},
        {"action_index": 2, "action_value": "客户公司拜访", "text": "客户公司拜访"},
        {"action_index": 3, "action_value": "客户来司拜访", "text": "客户来司拜访"},
        {"action_index": 4, "action_value": "在外约谈", "text": "在外约谈"},
        {"action_index": 5, "action_value": "实地拜访", "text": "实地拜访"}
    ]
    return options


def card_options_for_visit_types() -> list:
    """拜访类型"""
    options = [
        {"action_index": 1, "action_value": "初次拜访", "text": "初次拜访"},
        {"action_index": 2, "action_value": "签约后增量拜访", "text": "签约后增量拜访"},
        {"action_index": 3, "action_value": "签约后日常拜访", "text": "签约后日常拜访"},
        {"action_index": 4, "action_value": "签约前拜访", "text": "签约前拜访"}
    ]
    return options
