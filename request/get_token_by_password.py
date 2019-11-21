# coding=utf-8
"""
获取 access_token
"""

import os
import requests

CLIENT_ID = os.getenv('CLIENT_ID', '')
CLIENT_SECRET = os.getenv('CLIENT_SECRET', '')
auth = (CLIENT_ID, CLIENT_SECRET)

PORT = int(os.getenv('FLASK_RUN_PORT', 5000))

username = 'admin'
password = 'password'

data = {
    'grant_type': 'password',
    'username': username,
    'password': password,
    'scope': 'profile'
}
url = f'http://127.0.0.1:{PORT}/oauth/token'

# 申请token
"""
    POST /revoke HTTP/1.1
    Content-Type: application/x-www-form-urlencoded
    Authorization: Basic <client_id:client_secret>

    grant_type=password&username=username&password=password&scope=profile
"""
print('申请token')
res = requests.post(url, data=data, auth=auth)
print(res)
print(res.headers)
# {'access_token': '...', 'expires_in': 864000, 'scope': 'profile', 'token_type': 'Bearer'}
response_json = res.json()
print(response_json)

token = response_json['access_token']
token_type = response_json['token_type']


# 请求资源
"""
    POST /api HTTP/1.1
    Authorization: Bearer <access_token>
"""
print('请求资源')
url = f'http://127.0.0.1:{PORT}/api/me'
res = requests.get(url, headers={'Authorization': f'{token_type} {token}'})
print(res)
print(res.json())


# 撤销token
"""
    POST /revoke HTTP/1.1
    Content-Type: application/x-www-form-urlencoded
    Authorization: Basic <client_id:client_secret>

    token=45ghiukldjahdnhzdauz&token_type_hint=refresh_token
"""
print('撤销token')
url = f'http://127.0.0.1:{PORT}/oauth/revoke'
data = {
    'token': token
}
res = requests.post(url, data=data, auth=auth)
print(res)
print(res.json())
