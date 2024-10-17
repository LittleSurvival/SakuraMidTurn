from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Please replace LLAMA_CPP_SERVER_URL with the actual address and port of your LlamaCpp server
LLAMA_CPP_SERVER_URL = 'http://127.0.0.1:8080'

# Handle /v1/models requests
@app.route('/v1/models', methods=['GET'])
def get_models():
    # Forward GET request to the corresponding endpoint of the LlamaCpp server
    resp = requests.get(f'{LLAMA_CPP_SERVER_URL}/v1/models')

    # Return the response to the client
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]
    response = Response(resp.content, resp.status_code, headers)
    return response

# Solve /v1/chat/completions 
@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    # Get Requuest Data/Header
    data = request.get_data()
    headers = {key: value for key, value in request.headers if key != 'Host'}

    # Forward POST request to the corresponding endpoint of the LlamaCpp server
    resp = requests.post(f'{LLAMA_CPP_SERVER_URL}/v1/chat/completions',
                         data=data, headers=headers, stream=True)

    # Process the streaming response
    def generate():
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                yield chunk

    # Return the response to the client
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]
    return Response(generate(), resp.status_code, headers)

if __name__ == '__main__':
    for i in range(2,4):
        app.run(host=f'127.0.0.{i}', port=8080, threaded=True)
    
