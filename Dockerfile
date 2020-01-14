
# 创建时间：2020.01.24:

# python项目作为Resource或者Client通过接口或其他方式被调用，获取资源数据。对IdToken进行校验；
# 必须配置issuer信息，Resource端可以不配置client_id；Client端一定要配置client_id
# 本项目主要列举了放在接口装饰器形式和全局beforeRequest配置两种方式，也可以添加到装饰器中请自行添加；

FROM python:3.6

ADD requirements.txt /usr/src/
RUN pip install --no-cache-dir -r /usr/src/requirements.txt
WORKDIR /oidc-client
EXPOSE 5443

RUN mkdir -p /oidc-client
ADD keys /oidc-client/keys
ADD static /oidc-client/static
ADD templates /oidc-client/templates

# Empty conf
RUN echo "{}" >> /oidc-client/settings.json

# Most likely to be updated, do this last to not have to rebuild other layers
ADD *.py /oidc-client/

CMD ["python", "app.py"]