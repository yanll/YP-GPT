from typing import Dict

from dbgpt.util.lark import lark_message_util


def send_message_with_bingo(receive_id: str, template_variable: Dict):
    """包含点赞、新会话功能的消息卡片"""
    card = create_card_content_by_template("AAqkIdjGltfge", "1.0.16", template_variable)
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
        template_version_name="1.0.23",
        template_variable=template_variable
    )
    return lark_message_util.send_message(
        receive_id=receive_id,
        receive_id_type="open_id",
        content=card,
        msg_type="interactive"
    )

def send_message_with_welcome_rag(receive_id: str, template_variable: Dict):
    """欢迎卡片"""
    card = create_card_content_by_template(
        template_id="AAq3rrEyupkG1",
        template_version_name="1.0.2",
        template_variable=template_variable
    )
    return lark_message_util.send_message_rag(
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

def card_options_for_customer_service_levels() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "0", "text": "普通"},
        {"action_index": 2, "action_value": "1", "text": "VIP"},
        {"action_index": 3, "action_value": "2", "text": "SVIP"},
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

def card_options_for_meeting_room_name() -> list:
    """会议室的名称"""
    options = [
        {"action_index": 1, "action_value": "omm_fce8075d5a6a25c764a808c69a48b82a", "text": "Hacker"},
        {"action_index": 2, "action_value": "omm_435bca3a3d40f120c63540028b965538", "text": "smart"},
        {"action_index": 3, "action_value": "omm_d511e9e4e40f68107f556c943ca50c44", "text": "think different"},
        {"action_index": 4, "action_value": "omm_2fa172ec56aba79c654ec5a4b58e9f27", "text": "分享"},
        {"action_index": 5, "action_value": "omm_3864b3539c370d51e8d086791b008d44", "text": "北极星"},
        {"action_index": 6, "action_value": "omm_247693a0dbb368b6af624c51ba5df218", "text": "坦诚"},
        {"action_index": 7, "action_value": "omm_32be015ee6d9318e11561b984d665971", "text": "天权星"},
        {"action_index": 8, "action_value": "omm_dcf65c2ffcbabe4bf01c72e0470c541b", "text": "天枢星"},
        {"action_index": 9, "action_value": "omm_7e99a24f850323e3038526ce3f809ba5", "text": "天狼星"},
        {"action_index": 10, "action_value": "omm_fecbfd6505548d491026365ad03cb215", "text": "天玑星"},
        {"action_index": 11, "action_value": "omm_ddee0861011df191f0404b80f0c7d9eb", "text": "天璇星"},
        {"action_index": 12, "action_value": "omm_e457d7a3eb7133f98fc27a267a1646c1", "text": "天衡星"},
        {"action_index": 13, "action_value": "omm_d47dd4f223a3531f31b351513b036f61", "text": "太阳"},
        {"action_index": 14, "action_value": "omm_41510695cc2c9e86c3ef7d4afc247c74", "text": "尽责"},
        {"action_index": 15, "action_value": "omm_9da759bfae9935249eda2ce675e2682e", "text": "开放"},
        {"action_index": 16, "action_value": "omm_56bb92f696093b60a3108ae3b7102a78", "text": "开阳星"},
        {"action_index": 17, "action_value": "omm_2db12593ce9242345be73a59a0120ccc", "text": "摇光星"},
        {"action_index": 18, "action_value": "omm_4a260a86bc05a2d7dbb901c53bf5bc92", "text": "敢干"},
        {"action_index": 19, "action_value": "omm_001832945aef034f5853ca649db51b97", "text": "敢想"},
        {"action_index": 20, "action_value": "omm_5a1d13dc13e79e6f739b3d6f2d26c452", "text": "敢说"},
        {"action_index": 21, "action_value": "omm_1898ce77b933009c84cc999a93aeefc4", "text": "敢败"},
        {"action_index": 22, "action_value": "omm_a77aef5161de2d637bc0c156647474d4", "text": "极致"},
        {"action_index": 23, "action_value": "omm_bb38d0046d5159a31385030a1346a6c5", "text": "泰山"},
        {"action_index": 24, "action_value": "omm_a5ec3a14a94322968cd6fea05b34f4df", "text": "浪漫"},
        {"action_index": 25, "action_value": "omm_e8f296a80f0f448a9d6c659abb0a7ea8", "text": "禾口"},
        {"action_index": 26, "action_value": "omm_c520c17858b4b6fb22bac99f6e1dda5b", "text": "蓝点"},
        {"action_index": 27, "action_value": "omm_9ca36d25bfe178df5da26205b39da278", "text": "超越"},
        {"action_index": 27, "action_value": "omm_f15852ebf66fe58b2b23a01677d868d9", "text": "Beyond Innovative"},
        {"action_index": 28, "action_value": "omm_70f5c43c18a15e00eb4d95fafc9c5585", "text": "担当"},
        {"action_index": 29, "action_value": "omm_f016a5f4cc4ec85ed90960d3e07eaea4", "text": "时代"},
        {"action_index": 30, "action_value": "omm_7e2ecab8f9186315e257acf6f469fb77", "text": "星辰"},
        {"action_index": 31, "action_value": "omm_20655926a1f557cdbb2061658555ebeb", "text": "智能进化"},
        {"action_index": 32, "action_value": "omm_047d366f068f49683729f5bdf8d660f0", "text": "诚信"},
        {"action_index": 33, "action_value": "omm_88f18991716db9b7c543b80a1ce773b9", "text": "AI"},
        {"action_index": 34, "action_value": "omm_21c0b9e9f62bd9da13831c90c8ea0983", "text": "超越自我"},
        {"action_index": 35, "action_value": "omm_a751d42631e4801cd3061743fd9da429", "text": "高效协同"},

    ]


    return options


def card_options_for_meeting_room_data() -> list:
    """会议室的预定时间情况"""
    options = [
    {"action_index": 1, "action_value": "T00:00:00+08:00", "text": "00:00"},
    {"action_index": 2, "action_value": "T00:30:00+08:00", "text": "00:30"},
    {"action_index": 3, "action_value": "T01:00:00+08:00", "text": "01:00"},
    {"action_index": 4, "action_value": "T01:30:00+08:00", "text": "01:30"},
    {"action_index": 5, "action_value": "T02:00:00+08:00", "text": "02:00"},
    {"action_index": 6, "action_value": "T02:30:00+08:00", "text": "02:30"},
    {"action_index": 7, "action_value": "T03:00:00+08:00", "text": "03:00"},
    {"action_index": 8, "action_value": "T03:30:00+08:00", "text": "03:30"},
    {"action_index": 9, "action_value": "T04:00:00+08:00", "text": "04:00"},
    {"action_index": 10, "action_value": "T04:30:00+08:00", "text": "04:30"},
    {"action_index": 11, "action_value": "T05:00:00+08:00", "text": "05:00"},
    {"action_index": 12, "action_value": "T05:30:00+08:00", "text": "05:30"},
    {"action_index": 13, "action_value": "T06:00:00+08:00", "text": "06:00"},
    {"action_index": 14, "action_value": "T06:30:00+08:00", "text": "06:30"},
    {"action_index": 15, "action_value": "T07:00:00+08:00", "text": "07:00"},
    {"action_index": 16, "action_value": "T07:30:00+08:00", "text": "07:30"},
    {"action_index": 17, "action_value": "T08:00:00+08:00", "text": "08:00"},
    {"action_index": 18, "action_value": "T08:30:00+08:00", "text": "08:30"},
    {"action_index": 19, "action_value": "T09:00:00+08:00", "text": "09:00"},
    {"action_index": 20, "action_value": "T09:30:00+08:00", "text": "09:30"},
    {"action_index": 21, "action_value": "T10:00:00+08:00", "text": "10:00"},
    {"action_index": 22, "action_value": "T10:30:00+08:00", "text": "10:30"},
    {"action_index": 23, "action_value": "T11:00:00+08:00", "text": "11:00"},
    {"action_index": 24, "action_value": "T11:30:00+08:00", "text": "11:30"},
    {"action_index": 25, "action_value": "T12:00:00+08:00", "text": "12:00"},
    {"action_index": 26, "action_value": "T12:30:00+08:00", "text": "12:30"},
    {"action_index": 27, "action_value": "T13:00:00+08:00", "text": "13:00"},
    {"action_index": 28, "action_value": "T13:30:00+08:00", "text": "13:30"},
    {"action_index": 29, "action_value": "T14:00:00+08:00", "text": "14:00"},
    {"action_index": 30, "action_value": "T14:30:00+08:00", "text": "14:30"},
    {"action_index": 31, "action_value": "T15:00:00+08:00", "text": "15:00"},
    {"action_index": 32, "action_value": "T15:30:00+08:00", "text": "15:30"},
    {"action_index": 33, "action_value": "T16:00:00+08:00", "text": "16:00"},
    {"action_index": 34, "action_value": "T16:30:00+08:00", "text": "16:30"},
    {"action_index": 35, "action_value": "T17:00:00+08:00", "text": "17:00"},
    {"action_index": 36, "action_value": "T17:30:00+08:00", "text": "17:30"},
    {"action_index": 37, "action_value": "T18:00:00+08:00", "text": "18:00"},
    {"action_index": 38, "action_value": "T18:30:00+08:00", "text": "18:30"},
    {"action_index": 39, "action_value": "T19:00:00+08:00", "text": "19:00"},
    {"action_index": 40, "action_value": "T19:30:00+08:00", "text": "19:30"},
    {"action_index": 41, "action_value": "T20:00:00+08:00", "text": "20:00"},
    {"action_index": 42, "action_value": "T20:30:00+08:00", "text": "20:30"},
    {"action_index": 43, "action_value": "T21:00:00+08:00", "text": "21:00"},
    {"action_index": 44, "action_value": "T21:30:00+08:00", "text": "21:30"},
    {"action_index": 45, "action_value": "T22:00:00+08:00", "text": "22:00"},
    {"action_index": 46, "action_value": "T22:30:00+08:00", "text": "22:30"},
    {"action_index": 47, "action_value": "T23:00:00+08:00", "text": "23:00"},
    {"action_index": 48, "action_value": "T23:30:00+08:00", "text": "23:30"}
]




    return options


