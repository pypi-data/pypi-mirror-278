# xfapi 第三方库使用说明

## 一、概述

xfapi 是一个基于 FastAPI 框架开发的轻量级 RESTful API 框架。它允许通过 YAML 文件来配置 API 接口以及业务逻辑关联，并支持基础的 token 验证。xfapi 旨在提供高效、易用和可扩展的 API 开发体验。

## 二、安装

可以通过 pip 安装 xfapi：

```bash
pip install xfapi
```

## 三、配置文件示例

xfapi 使用 YAML 文件来配置 API 接口。以下是一个示例配置文件：

```yaml
apis:
- name: "token"
  path: "/token"
  method: "POST"
  handler: "apis.handler_token"

- name: "index"
  path: "/"
  method: "GET"
  handler: "apis.index"
```

- `name`: 接口的名称（可选）。
- `path`: 接口的路径。
- `method`: 请求方法（GET, POST, PUT, DELETE 等）。
- `handler`: 处理该接口的回调函数所在的模块和函数名（使用点号 `.` 分隔）。

## 四、回调函数示例

回调函数是处理 API 请求的逻辑函数。以下是一个简单的示例：

```python
from fastapi import Request
from xfapi.utils.auth import JWTUtils

def handler_token(data: dict):
    # token 方法示例(post)
    jwt = JWTUtils()
    token = jwt.encode_token({
        "data": data,
    })
    return {"token": token}

def index(request: Request):
    # get方法示例
    print(request.query_params)
    return {"data": "data"}

# ... 其他方法同理，支持 get, post, put, delete 等方法
```

- `data`: 在 POST 请求中，可以通过参数直接获取请求体数据。
- `request`: 在 GET 或其他请求中，可以通过 `Request` 对象获取请求信息。

## 五、调用示例

以下是如何使用 xfapi 启动服务器的示例：

```python
from xfapi.server import HTTPServer
from xfapi.utils.auth import TokenMiddleware

# 假设你已经有了 TokenMiddleware 的实现
token_middleware = TokenMiddleware()

# 创建一个 HTTPServer 实例，并传入 token 验证中间件
server = HTTPServer(auth_middleware=token_middleware.token_validation_middleware)

# 启动服务器
server.start()
```

在启动服务器后，xfapi 会根据 YAML 配置文件自动注册路由，并打印相关信息到控制台。

## 六、日志示例

服务器启动成功后，你可能会在控制台看到以下日志：

```log
INFO:xfapi.server:注册路由: /token POST -> apis.handler_token
INFO:xfapi.server:注册路由: / GET -> apis.index
INFO:     Started server process [43522]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 七、总结

xfapi 是一个基于 FastAPI 的轻量级 RESTful API 框架，它允许你通过 YAML 文件配置 API 接口和业务逻辑关联，并支持基础的 token 验证。使用 xfapi 可以帮助你更高效地构建、部署和维护 API 服务。希望这个使用说明能够帮助你快速上手 xfapi！