from flask import Flask, request, jsonify

app = Flask(__name__)

# 回调函数
def handle_data(data):
    # 在这里处理接收到的数据
    print("Received data:", data)
    # 返回处理结果
    return {"status": "success", "received_data": data}

@app.route('/receive_data', methods=['POST'])
def receive_data():
    # 获取请求中的JSON数据
    data = request.json
    # 调用回调函数处理数据
    response = handle_data(data)
    # 返回响应
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5670)
