# encoding: utf-8

##########################################################################
# 创建时间：2020.01.24:

# python项目作为Resource或者Client通过接口或其他方式被调用，获取资源数据。对IdToken进行校验；
# 必须配置issuer信息，Resource端可以不配置client_id；Client端一定要配置client_id
# 创建Oidc的Config配置信息，根据issuer返回的meta_data查询配置信息，初始化配置信息
# 本项目主要列举了放在接口装饰器形式和全局beforeRequest配置两种方式，也可以添加到装饰器中请自行添加；
##########################################################################

import os
import json
import tools
import urllib

class Config():

    _keys = ['api_endpoint',
            'authn_parameters',
            'authorization_endpoint',
            'base_url',
            'client_id',
            'client_secret',
            'dcr_client_id',
            'dcr_client_secret',
            'debug',
            'disable_https',
            'discovery_url',
            'issuer',
            'audience',
            'jwks_uri',
            'logout_endpoint',
            'port',
            'redirect_uri',
            'revocation_endpoint',
            'scope',
            'token_endpoint',
            'verify_ssl_server']

    def __init__(self, filename):
        self.filename = filename
        # self.init_config()



    def load_config(self):
        """
        Load config from file and environment
        :return:
        """
        self._load_from_file(self.filename)
        self._update_config_from_environment()

        if self.store['issuer'] is None or len(self.store['issuer']) == 0:
            raise ValueError('The expected token issuer must not be null')
        meta_data_url = self.store['issuer'] + '/.well-known/openid-configuration'
        ctx = tools.get_ssl_context(self.store)
        meta_data = urllib.request.urlopen(meta_data_url, context=ctx)
        if meta_data:
            self.store.update(json.load(meta_data))
        else:
            raise ValueError('Unexpected response on discovery document')
        if 'jwks_uri' not in self.store:
            raise ValueError('The expected token issuer must not be null')
        return self.store

    def _load_from_file(self, filename):
        print ('Loading settings from %s' % filename)
        self.store = json.loads(open(filename).read())

    def _update_config_from_environment(self):
        from_env = {}
        for key in self._keys:
            env = os.environ.get(key.upper(), None)
            if env:
                from_env[key] = env
        self.store.update(from_env)

    # def init_config(selfh):
    #     # config = Config(filepath)
    #     # filename = 'settings.json'
    #     # config = config.load_config()
    #     if self.config['issuer'] is None or len(config['issuer']) == 0:
    #         raise ValueError('The expected token issuer must not be null')
    #     meta_data_url = config['issuer'] + '/.well-known/openid-configuration'
    #     ctx = tools.get_ssl_context(config)
    #     meta_data = urllib.request.urlopen(meta_data_url, context=ctx)
    #     if meta_data:
    #         config.update(json.load(meta_data))
    #     else:
    #         raise ValueError('Unexpected response on discovery document')
    #     if 'jwks_uri' not in config:
    #         raise ValueError('The expected token issuer must not be null')
    #     return self
