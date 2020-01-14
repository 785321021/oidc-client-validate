# encoding: utf-8
#!/usr/bin/env python

# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(

    name="flask-oidc-validate",

    version="1.0",

    keywords='flask-oidc',

    description='A flask-oidc to validate IdToken for python ',

    author='lixin159',      # 替换为你的Pypi官网账户名
    author_email='785321021@qq.com',  # 替换为你Pypi账户名绑定的邮箱

    url='http://gitlab.it.taikang.com/iaa/oidc-client-python.git',

    long_description=open('README.md', encoding='utf-8').read(),

    packages=find_packages(),

    license='MIT'

)