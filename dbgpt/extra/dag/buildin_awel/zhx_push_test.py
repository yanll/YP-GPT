
import requests

# 请求的数据，根据你的接口需要进行相应的设置
data = {
    }

# 发送 POST 请求
response = requests.post("http://127.0.0.1:5670/api/v1/awel/trigger/lark_hanglv_monitor_daily_push_event", json=data)

# 输出响应结果
print(response.status_code)
print(response.json())



