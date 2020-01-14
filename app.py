# encoding: utf-8

from flask import Flask

app = Flask(__name__)

from flask_oidc_validate.OidcConfig import Config
config = Config('settings.json').load_config()
# config = config.load_config()

from flask_oidc_validate.IdTokenValidatorForRs import IdTokenValidatorForRs

# '''接口上加装饰器'''
# token_validator = IdTokenValidatorForRs(config)
# @app.route('/test')
# @token_validator.validate()
# def testAPI():
#     return 'success'

'''全局配置过滤器'''
token_validator = IdTokenValidatorForRs(config, app=app)
@app.route('/test')
def testAPI():
    return 'success'


if __name__ == '__main__':
    port = 5443
    app.run('0.0.0.0', port=port)

