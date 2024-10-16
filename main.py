from flask import Flask, request, Response
import requests

app = Flask(__name__)

# 请将LLAMA_CPP_SERVER_URL替换为您的LlamaCpp服务器实际地址和端口
LLAMA_CPP_SERVER_URL = 'http://127.0.0.1:8080'

# 处理 /v1/models 请求
@app.route('/v1/models', methods=['GET'])
def get_models():
    # 转发GET请求到LlamaCpp服务器的对应端点
    resp = requests.get(f'{LLAMA_CPP_SERVER_URL}/v1/models')

    # 将响应返回给客户端
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]
    response = Response(resp.content, resp.status_code, headers)
    return response

# 处理 /v1/chat/completions 请求
@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    # 获取请求数据和头信息
    data = request.get_data()
    headers = {key: value for key, value in request.headers if key != 'Host'}

    # 转发POST请求到LlamaCpp服务器的对应端点
    resp = requests.post(f'{LLAMA_CPP_SERVER_URL}/v1/chat/completions',
                         data=data, headers=headers, stream=True)

    # 处理流式响应
    def generate():
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                yield chunk

    # 将响应返回给客户端
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]
    return Response(generate(), resp.status_code, headers)

if __name__ == '__main__':
    app.run(host='127.0.0.2', port=8080, threaded=True)
