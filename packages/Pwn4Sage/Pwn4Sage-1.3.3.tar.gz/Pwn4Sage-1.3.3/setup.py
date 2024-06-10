#!python
# -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages
import Pwn4Sage

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="Pwn4Sage",
    version=Pwn4Sage.__version__,
    author="Harry0597",
    author_email="1915885792@qq.com",
    description="A simplified Pwntools for SageMath",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/Harry0597/Pwn4Sage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)

