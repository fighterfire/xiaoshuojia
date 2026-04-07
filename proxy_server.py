#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI API 代理服务器
用于解决浏览器跨域问题，将请求转发到目标API服务器

使用方法:
1. 安装依赖: pip install flask flask-cors
2. 运行服务器: python proxy_server.py
3. 在小说家设置中开启"使用本地代理"
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import sys

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST', 'OPTIONS'])
def proxy():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        
        api_key = data.get('apiKey')
        base_url = data.get('baseUrl', 'https://api.siliconflow.cn/v1')
        model = data.get('model', 'deepseek-ai/DeepSeek-V3')
        messages = data.get('messages', [])
        max_tokens = data.get('max_tokens', 800)
        temperature = data.get('temperature', 0.8)
        
        if not api_key:
            return jsonify({'error': {'message': '缺少API Key'}}), 400
        
        api_url = base_url.rstrip('/') + '/chat/completions'
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        payload = {
            'model': model,
            'messages': messages,
            'max_tokens': max_tokens,
            'temperature': temperature
        }
        
        print(f"[请求] {api_url}")
        print(f"[模型] {model}")
        
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        print(f"[状态] {response.status_code}")
        
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.Timeout:
        return jsonify({'error': {'message': '请求超时'}}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': {'message': f'网络错误: {str(e)}'}}), 502
    except Exception as e:
        return jsonify({'error': {'message': f'服务器错误: {str(e)}'}}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("=" * 50)
    print("  小说家 AI API 代理服务器")
    print("=" * 50)
    print()
    print("服务地址: http://localhost:8080")
    print()
    print("使用说明:")
    print("1. 确保已安装依赖: pip install flask flask-cors requests")
    print("2. 在小说家设置中开启'使用本地代理'")
    print("3. 保持此窗口运行")
    print()
    print("按 Ctrl+C 停止服务器")
    print("=" * 50)
    
    try:
        app.run(host='127.0.0.1', port=8080, debug=False)
    except KeyboardInterrupt:
        print("\n服务器已停止")
        sys.exit(0)
