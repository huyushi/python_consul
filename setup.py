# -*- coding: utf-8 -*-
# Author: yushi
# Date: 2021/1/12

from setuptools import setup, find_packages

setup(
    name="consul_service",
    version="0.0.2",
    keywords=("pip", "defensor", "yushi", "ms"),
    description="python版本的consul服务中心接口",
    long_description="",
    license="MIT Licence",
    url="https://github.com/DiligentApprentice",
    author="yushi.hu",
    author_email="yushi.hu@flexiv.com",
    packages=find_packages(),
    install_requires=[
        "python-consul==1.1.0",
        "requests==2.25.1"

    ]
)
