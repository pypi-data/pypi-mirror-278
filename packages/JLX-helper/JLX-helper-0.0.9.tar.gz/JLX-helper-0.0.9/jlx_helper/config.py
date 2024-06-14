# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  JLX-helper
# FileName:     config.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/06/07
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""

url_map = {
    "procotol": "http",
    "auth_username": "yundou",
    "auth_password": "jlx123",
    "domain": "ticket.jiulvxing.com",
    "get_authorization_token": "/ticket/auto/getApiUserToken",  # 获取token
    "get_query_quotation": "/purchaseApi/search",  # 获取查询报价
    "push_sms": "/purchaseApi/sms",  # 推送含有验证码的短信原文
    "gen_service_order": "/purchaseApi/order",  # 生成订单
    "payment_service_order": "/purchaseApi/pay",  # 支付订单
    "get_itinerary_info": "/purchaseApi/ticket",  # 查询票号
}

card_type_map = {
    "护照": "PP",
    "未知": "NONE",
    "军人证": "JR",
    "回乡证": "HX",
    "身份证": "NI",
    "户口簿": "HR",
    "出生证明": "BC",
    "国际海员证": "HY",
    "港澳通行证": "GA",
    "港澳台居住证": "HM",
    "港澳台居民居住证": "HM",
    "外国人永久居留证": "LW",
    "外国人永久居留身份证": "LW",
    "大陆居民往来台湾通行证": "TW",
}

age_type_map = {
    "成人": "ADULT",
    "儿童": "CHILD",
    "婴儿": "INFANT",
    "留学生": "OVERSEAS"
}
