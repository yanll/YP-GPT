import requests
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from dbgpt.app.openapi.api_view_model import Result

ignored_exp = [
    "/apidoc",
    "/api/controller/heartbeat"
]


def principal(token):
    url = 'http://ycenc.yeepay.com:30422/yuia-service-boss/auth/principal'
    headers = {
        'systemcode': 'iam-console',
        'yuiassotoken': token
    }
    params = {}
    resp = requests.post(url=url, headers=headers, params=params)
    return resp.json()


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """ 用户认证"""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        """ 认证信息 """
        path = request.url.path
        if path in ignored_exp:
            return await call_next(request)
        token = request.headers.get("Authorization", "")
        if token == "":
            print("认证信息为空，请重新登录！", path)
            res = Result.failed(code="401", msg="认证信息为空，请重新登录！")
            return JSONResponse(status_code=200, content=res.dict())

        resp = principal(token)
        if (resp['code'] != 200):
            print("认证信息已过期，请重新登录！", path)
            res = Result.failed(code="401", msg="认证信息已过期，请重新登录！")
            return JSONResponse(status_code=200, content=res.dict())
        result = await call_next(request)
        return result
