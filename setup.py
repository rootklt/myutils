#!/usr/bin/env python3
#coding:utf-8

import os
import sys
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

readme_file = os.path.join(here, 'README.md')

def read_text(file_path):
    """
    fix the default operating system encoding is not utf8.
    """
    if sys.version_info.major < 3:
        with open(file_path) as f:
            return f.read()
    with open(file_path, encoding="utf8") as f:
        return f.read()

README = read_text(os.path.join(here, 'README.md'))

requires = read_text(os.path.join(here, 'requirements.txt')) # 依赖文件

test_requirements = [

]


setup(
    name='myutils',
    description='some util tools',
    version='1.0.1',
    author='rootklt',
    author_email='xx@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    long_description=README,
    url='https://github.com/rootklt/myutils',
    install_requires=requires,
    tests_require=test_requirements,
    platforms='all platform',
    python_requires = '>=3.5.0',
    license='BSD',
)
