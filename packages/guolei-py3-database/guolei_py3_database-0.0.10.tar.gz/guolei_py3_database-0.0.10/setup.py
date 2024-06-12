#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name="guolei_py3_database",
      version="0.0.10",
      description="a python3 database library by guolei",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/guolei19850528/guolei_py3_database",
      author="guolei",
      author_email="174000902@qq.com",
      license="MIT",
      keywors=["PyMySQL", "redis","sqlite"],
      packages=setuptools.find_packages('./'),
      install_requires=["PyMySQL", "redis"],
      python_requires='>=3.0',
      zip_safe=False)
