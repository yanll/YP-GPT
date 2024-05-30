
import requests
from dbgpt.util.lark import larkutil
def get_email(name):
    url = "http://ycenc.yeepay.com:8606/ai-assistants/uia/get_user_by_key?key=%E4%B8%A5%E4%BA%AE%E4%BA%AE&key_type=cn_name"  # 目标URL
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'app_key': "ai-assistants",
        'app_secret': "fcd2f6kd0c3acf1c"
    }
    params = {
        'key': name,
        'key_type': 'cn_name'
    }  # 传递的参数
    try:
        response = requests.get(url, params=params, headers = headers)  # 发送GET请求，带上参数
        response.raise_for_status()  # 如果请求失败，抛出异常
        data = response.json()  # 假设返回的是JSON数据
        # 处理你想要的信息
        email = data['data']['email'] # 假设想要的信息在JSON中的字段名为'desired_field'
        if isinstance(email, str):
            email = [email]  # 如果邮箱地址是字符串，将其包装在列表中
        print("获取到的信息是:", email)
        return email

    except requests.exceptions.RequestException as e:
        print("请求失败:", e)





# 获取访问令牌
tokens = larkutil.get_tenant_access_token()
token = tokens['tenant_access_token']
def get_user_open_id(name):
    emails = get_email(name)
    url = 'https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    data = {
        "emails": emails,
        "include_resigned": True,
        "mobiles": []
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        # 检查响应数据是否包含所需的结构
        if response_data.get('code') == 0 and 'data' in response_data and 'user_list' in response_data['data']:
            user_list = response_data['data']['user_list']
            user_dict = {}
            for user in user_list:
                # 检查每个用户字典中是否存在'email'和'user_id'
                if 'email' in user and 'user_id' in user:
                    user_dict[user['email']] = user['user_id']
                else:
                    # 如果缺少'email'或'user_id'，可以记录日志或抛出异常
                    print(f"Missing 'email' or 'user_id' in user data: {user}")
            return user_dict
        else:
            # 如果响应数据中没有user_list或code不为0，则返回错误信息
            return {'error': 'Invalid response format'}
    else:
        # 请求失败，返回None或错误信息
        return {'error': f'Request failed with status code {response.status_code}'}


# result = get_user_open_id(name = '张华雪')
#
# print(result)

