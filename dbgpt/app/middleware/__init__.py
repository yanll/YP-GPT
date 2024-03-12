from fastapi import FastAPI

from .authentication_middleware import AuthenticationMiddleware
from .usetime_middleware import UseTimeMiddleware


def registerMiddlewareHandle(server: FastAPI):
    # 添加中间件，先注册的后执行
    server.add_middleware(UseTimeMiddleware)
    server.add_middleware(AuthenticationMiddleware)
