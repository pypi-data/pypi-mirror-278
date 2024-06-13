# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  JLX-helper
# FileName:     utils.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/06/07
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import re
from datetime import datetime

dt_standar_format = '%Y-%m-%d %H:%M:%S'


def covert_dict_key_to_lower(d: dict) -> dict:
    result = dict()
    for key, value in d.items():
        if isinstance(key, str):
            key_new = key.lower()
            result[key_new] = value
    return result


def get_html_title(html: str) -> str:
    # 使用正则表达式提取目标字符串
    pattern = '<title>(.*?)</title>'
    match = re.search(pattern, html)
    if match:
        title = match.group(1)
    else:
        title = "Abnormal HTML document structure"
    return title


def timestamp_to_datetime(timestamp: int) -> datetime:
    if len(str(timestamp)) == 13:
        # 将 13 位时间戳转换为秒
        timestamp = timestamp / 1000.0

    # 将时间戳转换为 datetime 对象
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object


def timestamp_to_datetime_str(timestamp: int) -> str:
    dt_object = timestamp_to_datetime(timestamp=timestamp)
    return dt_object.strftime(dt_standar_format)
