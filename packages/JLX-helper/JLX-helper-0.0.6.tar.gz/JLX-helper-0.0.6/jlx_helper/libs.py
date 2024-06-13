# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  JLX-helper
# FileName:     libs.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/06/07
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import logging

# 定义日志格式
log_format = "%(asctime)s - [%(levelname)s] - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# 配置日志设置
logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=date_format)

logger = logging.getLogger("root")
