# oidc-client-python

基于python语言的oidc授权认证

创建时间：2020.01.24:

python项目作为Resource或者Client通过接口或其他方式被调用，获取资源数据。对IdToken进行校验；
必须配置issuer信息，Resource端可以不配置client_id；Client端一定要配置client_id
本项目主要列举了放在接口装饰器形式和全局beforeRequest配置两种方式，也可以添加到装饰器中请自行添加；

直接下载项目 python app.py可以启动测试例子
测试接口为 http://localhost:5443/test  （要在Headers里配置  Authorization：Bearer +你的IdToken）


