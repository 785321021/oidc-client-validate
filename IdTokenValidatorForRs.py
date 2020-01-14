# encoding: utf-8
##########################################################################
# 创建时间：2020.01.24:

# python项目作为Resource通过接口或其他方式被调用，获取资源数据。对IdToken进行校验；
# 必须配置issuer信息，Resource端可以不配置client_id；Client端一定要配置client_id
# Resource端不校验client_id；
# 本项目主要列举了放在接口装饰器形式和全局beforeRequest配置两种方式，也可以添加到装饰器中请自行添加；
##########################################################################

import json
import urllib
import flask
import time
from jwkest import BadSignature
from jwkest.jwk import KEYS
from jwkest.jws import JWS
from tools import base64_urldecode
from tools import get_ssl_context
from functools import wraps
from flask import request, jsonify


class IdTokenValidatorForRs(object):
    """
    Resource端校验IdToken类
    """

    def __init__(self, config, app=None):
        self.config = config
        self.DEFAULT_MAX_CLOCK_SKEW = 60
        self.expectedIssuer = self.config['issuer']
        self.jwks_uri = self.config['jwks_uri']
        self.ctx = get_ssl_context(self.config)
        self.jwks = self.load_keys()
        if app is not None:
            app.before_request(self._before_request)

    def _before_request(self):
        """
        before_request方法拦截所有请求，对所有请求进行校验
        """
        id_token = None
        if 'Authorization' in request.headers and request.headers['Authorization'].startswith('Bearer '):
            id_token = request.headers['Authorization'].split(None, 1)[1].strip()
        if 'id_token' in request.form:
            id_token = request.form['id_token']
        elif 'id_token' in request.args:
            id_token = request.args['id_token']
        if id_token:
            # 解析token
            valid = self.jwtValidate(id_token)
            if valid is None:
                return
            else:
                errorInfo = {"error": "invalid_token", "error_description": valid}
                result = jsonify(errorInfo=errorInfo)
                return result, 403, {'WWW-Authenticate': 'Bearer'}
        else:
            errorInfo = {"error": "login_required", "error_description": 'Missing Token'}
            result = jsonify(code=401, errorInfo=errorInfo)
            return flask.make_response(result)

    def validate(self):
        """
        validate方法，作为装饰器装饰需要的方法，对所有请求进行校验
        """

        def wrapper(view_func):
            @wraps(view_func)
            def decorated(*args, **kwargs):
                # 获取token
                id_token = None
                if 'Authorization' in request.headers and request.headers['Authorization'].startswith('Bearer '):
                    id_token = request.headers['Authorization'].split(None, 1)[1].strip()
                if 'id_token' in request.form:
                    id_token = request.form['id_token']
                elif 'id_token' in request.args:
                    id_token = request.args['id_token']
                if id_token:
                    # 解析token
                    valid = self.jwtValidate(id_token)
                    if valid is None:
                        return view_func(*args, **kwargs)
                    else:
                        errorInfo = {"error": "invalid_token", "error_description": valid}
                        result = jsonify(errorInfo=errorInfo)
                        return result, 403, {'WWW-Authenticate': 'Bearer'}
                else:
                    errorInfo = {"error": "login_required", "error_description": 'Missing Token'}
                    result = jsonify(code=401, errorInfo=errorInfo)
                    return flask.make_response(result)

            return decorated

        return wrapper

    def jwtValidate(self, token):
        """
        jwt方式解析token

        :param token: 需要解析的token.
        :type field: str
        :returns: 解析成功返回None；解析失败返回错误信息.
        :rtype: object

        .. versionadded:: 1.0
        """
        parts = token.split('.')
        if len(parts) != 3:
            raise BadSignature('Invalid JWT. Only JWS supported.')
        header = json.loads(base64_urldecode(parts[0]))
        payload = json.loads(base64_urldecode(parts[1]))
        # 校验 issuer
        if self.expectedIssuer != payload['iss']:
            return "Invalid issuer %s, expected %s" % (payload['iss'], self.expectedIssuer)
        # 校验过期时间
        if int(time.time()) >= int(payload['exp']):
            return "Token has expired"
        # 校验生效时间
        if int(time.time()) <= int(payload['iat']):
            return "Token issued in the past"

        jws = JWS(alg=header['alg'])
        try:
            jws.verify_compact(token, self.jwks)
            return
        except Exception as e:
            # 第一次解析异常时，更新jwks信息重新解析
            try:
                self.jwks = self.load_keys()
                jws.verify_compact(token, self.jwks)
                return
            except Exception as e:
                return 'Invalid token!'

    def load_keys(self):
        # load the jwk set.
        jwks = KEYS()
        jwks.load_jwks(self.get_jwks_data())
        return jwks

    def get_jwks_data(self):
        request = urllib.request.Request(self.jwks_uri)
        request.add_header('Accept', 'application/json')
        request.add_header('User-Agent', 'CurityExample/1.0')

        try:
            jwks_response = urllib.request.urlopen(request, context=self.ctx)
        except Exception as e:
            print("Error fetching JWKS", e)
            raise e
        return jwks_response.read()
