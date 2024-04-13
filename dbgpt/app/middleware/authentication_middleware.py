import requests
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from dbgpt.app.openapi.api_view_model import Result
from dbgpt.app.user.service import UserService
from dbgpt.util.sutil import ssourl, enabledsso

ignored_exp = [
    "/favicon.ico",
    "/apidoc",
    "/api/controller/heartbeat",
    "/_next/static"
]

user_service = UserService()


def principal(token):
    headers = {
        'systemcode': 'iam-console',
        'yuiassotoken': token
    }
    params = {}
    resp = requests.post(url=ssourl(), headers=headers, params=params)
    return resp.json()


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """ 用户认证"""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        """ 认证信息 """
        if not enabledsso():
            return await call_next(request)
        path = request.url.path
        if any(path.startswith(exp) for exp in ignored_exp):
            return await call_next(request)

        if (path.startswith("/api/v1/awel/trigger")):
            credential = ""
            # if (credential != "123456"):
            #     print("应用访问令牌非法！", path)
            #     res = Result.failed(code="401", msg="应用访问令牌非法！")
            #     return JSONResponse(status_code=200, content=res.dict())
            return await call_next(request)

        token = request.headers.get("Authorization", "")
        if token == "":
            print("认证信息为空，请重新认证！", path)
            res = Result.failed(code="401", msg="认证信息为空，请重新认证！")
            return JSONResponse(status_code=200, content=res.dict())
        resp = principal(token)
        if (resp['code'] != 200):
            print("认证信息已过期，请重新认证！", path)
            res = Result.failed(code="401", msg="认证信息已过期，请重新认证！")
            return JSONResponse(status_code=200, content=res.dict())

        user = resp['data']
        loginuser = user['loginName']
        # 校验用户清单
        users = user_service.get_user()
        usernames = [user.username for user in users]
        if loginuser not in usernames:
            print("您的账户暂未激活，请联系系统管理员！", loginuser, path)
            res = Result.failed(code="ACCOUNT_INACTIVATED", msg="您的账户暂未激活，请联系系统管理员！")
            return JSONResponse(status_code=200, content=res.dict())
        result = await call_next(request)
        return result
