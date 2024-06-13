# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  JLX-helper
# FileName:     setup.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/06/07
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from setuptools import setup, find_packages

setup(
    name='JLX-helper',
    version='0.0.4',
    description='This is my JLX help package',
    long_description='This is my JLX help package',
    author='ckf10000',
    author_email='ckf10000@sina.com',
    url='https://github.com/ckf10000/JLX-helper',
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
