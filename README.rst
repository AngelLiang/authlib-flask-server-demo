authlib 示例代码
#################


操作步骤
*********

1. 安装环境::

    pipenv install


2. 运行服务端::

    # console 1
    pipenv shell
    flask initdb
    flask run


3. 访问 http://127.0.0.1:5000/ 创建默认的用户名：admin，后面会用到

4. 访问 http://127.0.0.1:5000/admin/oauth2client/ 创建 client

表单填写如下

- client_name: remote
- client_uri: http://127.0.0.1:8000/
- allowed_scope: profile
- redirect_uris: http://127.0.0.1:8000/auth
- allowed_grant_types: authorization_code
- allowed_response_types: code
- token_endpoint_auth_method: client_secret_basic


5. 复制生成的 client_id 和 client_secret 到 当前目录下的 .env 文件，如果没有则创建::

    # .env
    CLIENT_ID = ...
    CLIENT_SECRET = ...

6. 启动 client.py::

    # console 2
    pipenv shell
    python client/client.py


7. 访问 http://127.0.0.1:8000/ ，然后 login

8. consent 打钩，输入 admin 用户名，提交

9. 返回由 app 生成的 access_token 等信息的json

10. 资源访问测试

    1. 访问 http://127.0.0.1:8000/me 获取用户名
    2. 访问 http://127.0.0.1:8000/profile 获取有 profile 作用域（scope）的资源

11. 结束
