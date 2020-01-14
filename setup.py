# encoding: utf-8
#!/usr/bin/env python

# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(

    name="flask-oidc-validator",

    version="1.2",

    keywords='flask-oidc',

    description='A flask-oidc to validate IdToken for python ',

    author='lixin159',
    author_email='785321021@qq.com',

    url='https://github.com/785321021/oidc-client-validate.git',

    long_description=open('README.md', encoding='utf-8').read(),

    packages=find_packages(),

    license='MIT'

)