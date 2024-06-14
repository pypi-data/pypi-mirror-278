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
from jlx_helper.libs import date_format

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
    return dt_object.strftime(date_format)


def get_age(birth_date: str = None, card_id: str = None) -> int:
    # 获取当前日期
    today = datetime.today()
    if birth_date:
        if len(birth_date) == 10:
            birth_date = "{} 00:00:00".format(birth_date, today)
        else:
            if len(birth_date) > 19:
                return -99
    else:
        if isinstance(card_id, str) and len(card_id) == 18:
            birth_date = "{}-{}-{} 00:00:00".format(card_id[6:10], card_id[10:12], card_id[12:14])
        else:
            return -99
    birth_dt = datetime.strptime(birth_date, date_format)
    # 计算年龄
    age = today.year - birth_dt.year
    # 检查是否已经过了生日
    if today.month < birth_dt.month or (today.month == birth_dt.month and today.day < birth_dt.day):
        age -= 1
    return age


def get_gender_code(gender: str) -> str:
    if gender.lower() in ['M', '男', "male"]:
        return 'male'
    elif gender.lower() in ['F', '女', "female"]:
        return 'female'
    else:
        return ''
