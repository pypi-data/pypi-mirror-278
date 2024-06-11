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
