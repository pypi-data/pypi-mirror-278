# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  JLX-helper
# FileName:     api.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/06/07
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from jlx_helper.http_client import HttpService


class JLXApi(object):

    def __init__(self, domain: str, protocol: str) -> None:
        self.__http_client = HttpService(domain=domain, protocol=protocol)

    def get_authorization_token(self, path: str, method: str, user: str, password: str) -> dict:
        """
        获取认证token
        :param str path: 调用api接口的url后缀
        :param str method: 调用api的http请求方法
        :param str user: 请求参数
        :param str password: 请求参数
        :return: dict
        """
        # 要发送的表单数据
        form_data = {
            'userName': user,
            'password': password
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        return self.__http_client.send_request(method=method, path=path, data=form_data, headers=headers)

    def get_query_quotation(self, path: str, method: str, token: str, ticket_channel: str, channel_user: str,
                            channel_password: str, departure_city_code: str, arrive_city_code: str, departure_date: str,
                            flight_no: str, cabin: str = None, channel_token: str = None, product_type: str = "cpa",
                            trip_type: str = "single_trip") -> dict:
        """
        获取查询报价
        :param str path: 调用api接口的url后缀
        :param str method: 调用api的http请求方法
        :param str token: 调用api所需要的认证token
        :param str ticket_channel: 询价渠道，jlx:就旅行,bsp:bsp,qunarwn:蜗牛,qunarm:去哪儿M网,tongchengcg:同程分销,
                                   book51:51BOOK,hbgj:hbgj,b2b:b2b,b2c:b2c,yibao_b2b:易宝b2b,spider_b2b:自有自动B2B,
                                   spider_b2c:自有自动B2C,qunarApp:去哪APP,tdQunarApp:通达去哪APP,ctrip:携程,
                                   jlx_ctrip:自有携程,feizhum:飞猪M,tongchengapp:同程APP,ctripapp:携程APP,
                                   tongchenggift:同程礼品卡,jinghang:京杭,feizhuyd:飞猪永动,jegotrip:无忧行,
                                   spider_b2b_nopnr:自有白屏B2B,tcapp:同程APP熊大,ept:E票通B2B,czndc:南航NDC,
                                   jlx_tc_app:就旅行同程APP,meituan:美团分销,jlx_xc_app:就旅行携程APP
        :param str channel_user: 渠道用户
        :param str channel_password: 渠道用户密码
        :param str departure_city_code: 起飞城市编码
        :param str arrive_city_code: 抵达城市编码
        :param str departure_date: 起飞日期，YYYY-MM-DD
        :param str flight_no: 航班号
        :param str cabin: 舱位类型，某些平台需要指定舱位类型
        :param str channel_token: 渠道认证Token
        :param str product_type: 产品类型，cpc(标准)、cpa(特价)、special(特殊)
        :param str trip_type: 行程类型，single_trip(单程)、round_trip(往返)
        :return: dict
        """
        headers = dict(Authorization=token)
        channel_user_info = dict(name=channel_user, pwd=channel_password)
        if channel_token:
            channel_user_info['token'] = channel_token
        segment = dict(
            dpt=departure_city_code,  # XIY
            arr=arrive_city_code,  # ZHA
            date=departure_date,  # 2024-06-13
            flightNum=flight_no,  # UQ3528
        )
        if cabin:
            segment['cabin'] = cabin  # Y/E
        json = {
            "productType": product_type,
            "ticketChannel": ticket_channel,  # jlx_xc_app|qunarm
            "ticketUser": channel_user_info,
            "tripType": trip_type,
            "segments": [segment]
        }
        return self.__http_client.send_request(method=method, path=path, json=json, headers=headers)

    def push_sms(self, path: str, method: str, token: str, sms_content: str, phone: str) -> dict:
        """
        推送验证码短信原文
        :param str path: 调用api接口的url后缀
        :param str method: 调用api的http请求方法
        :param str token: 调用api所需要的认证token
        :param sms_content: 短信原文
        :param phone: 接收短信的手机号
        :return: dict
        """
        headers = dict(Authorization=token)
        json = {
            "context": sms_content,
            "phomeNum": phone
        }
        return self.__http_client.send_request(method=method, path=path, json=json, headers=headers)

    def gen_service_order(self, path: str, method: str, token: str, ticket_channel: str, channel_user: str,
                          order_id: str, departure_city_code: str, arrive_city_code: str, departure_date: str,
                          flight_no: str, passengers: list, internal_phone: str, price_context: str = None,
                          conditions: list = None, cabin: str = None, trip_type: str = "single_trip"):
        """
        生成就旅行订单
        :param str path: 调用api接口的url后缀
        :param str method: 调用api的http请求方法
        :param str token: 调用api所需要的认证token
        :param str ticket_channel: 询价渠道，jlx:就旅行,bsp:bsp,qunarwn:蜗牛,qunarm:去哪儿M网,tongchengcg:同程分销,
                                   book51:51BOOK,hbgj:hbgj,b2b:b2b,b2c:b2c,yibao_b2b:易宝b2b,spider_b2b:自有自动B2B,
                                   spider_b2c:自有自动B2C,qunarApp:去哪APP,tdQunarApp:通达去哪APP,ctrip:携程,
                                   jlx_ctrip:自有携程,feizhum:飞猪M,tongchengapp:同程APP,ctripapp:携程APP,
                                   tongchenggift:同程礼品卡,jinghang:京杭,feizhuyd:飞猪永动,jegotrip:无忧行,
                                   spider_b2b_nopnr:自有白屏B2B,tcapp:同程APP熊大,ept:E票通B2B,czndc:南航NDC,
                                   jlx_tc_app:就旅行同程APP,meituan:美团分销,jlx_xc_app:就旅行携程APP
        :param str channel_user: 渠道用户
        :param str order_id: 订单id
        :param str departure_city_code: 起飞城市编码
        :param str arrive_city_code: 抵达城市编码
        :param str departure_date: 起飞日期，YYYY-MM-DD
        :param str flight_no: 航班号
        :param list passengers: 预订机票的乘客信息
        :param str internal_phone: 公司售后电话号码，接收航变信息
        :param str price_context: 查询报价上下文，从报价接口直接获取，某平台需要
        :param list conditions: 生成订单的条件
        :param str cabin: 舱位类型，某些平台需要指定舱位类型
        :param str trip_type: 行程类型，single_trip(单程)、round_trip(往返)
        :return: dict
        """
        headers = dict(Authorization=token)
        segment = dict(
            dpt=departure_city_code,  # XIY
            arr=arrive_city_code,  # ZHA
            date=departure_date,  # 2024-06-13
            flightNum=flight_no,  # UQ3528
        )
        if cabin:
            segment['cabin'] = cabin  # Y/E
        json = {
            "yourOrderNo": order_id,
            "passengers": passengers,
            "segments": [segment],
            "ticketChannel": ticket_channel,
            "ticketUser": {
                "name": channel_user
            },
            "tripType": trip_type,
            "contactPhone": internal_phone
        }
        if price_context:
            json["priceContext"] = price_context
        if conditions:
            json['conditions'] = conditions
        return self.__http_client.send_request(method=method, path=path, json=json, headers=headers)

    def payment_service_order(self, path: str, method: str, token: str, ticket_channel: str, channel_user: str,
                              jlx_order_id: str, pay_type: str, bank_card_info: dict = None,
                              pay_user_info: dict = None) -> dict:
        """
        支付就旅行订单
        :param str path: 调用api接口的url后缀
        :param str method: 调用api的http请求方法
        :param str token: 调用api所需要的认证token
        :param str ticket_channel: 询价渠道，jlx:就旅行,bsp:bsp,qunarwn:蜗牛,qunarm:去哪儿M网,tongchengcg:同程分销,
                                   book51:51BOOK,hbgj:hbgj,b2b:b2b,b2c:b2c,yibao_b2b:易宝b2b,spider_b2b:自有自动B2B,
                                   spider_b2c:自有自动B2C,qunarApp:去哪APP,tdQunarApp:通达去哪APP,ctrip:携程,
                                   jlx_ctrip:自有携程,feizhum:飞猪M,tongchengapp:同程APP,ctripapp:携程APP,
                                   tongchenggift:同程礼品卡,jinghang:京杭,feizhuyd:飞猪永动,jegotrip:无忧行,
                                   spider_b2b_nopnr:自有白屏B2B,tcapp:同程APP熊大,ept:E票通B2B,czndc:南航NDC,
                                   jlx_tc_app:就旅行同程APP,meituan:美团分销,jlx_xc_app:就旅行携程APP
        :param str channel_user: 渠道用户
        :param str jlx_order_id: 就旅行订单id
        :param str pay_type: 支付类型，BALANCE:余额,weixin:微信,ALI_PAY:支付宝,creditcard:信用卡,YI_BAO:易宝,HUI_FU:汇付,
                                    YI_BAO_XINYONG:易宝信用,HUIFU_OTA:汇付签约,tabao_charge:淘宝代付
        :param dict bank_card_info: 信用卡信息
        :param dict pay_user_info: 第三方支付信息，如易宝会员支付
        :return: dict
        """
        headers = dict(Authorization=token)
        json = {
            "orderNo": jlx_order_id,
            "payType": pay_type,
            "ticketChannel": ticket_channel,
            "ticketUser": {
                "name": channel_user
            }
        }
        if bank_card_info:
            json['bankCardInfo'] = bank_card_info
        if pay_user_info:
            json['payUser'] = pay_user_info
        return self.__http_client.send_request(method=method, path=path, json=json, headers=headers)

    def get_itinerary_info(self, path: str, method: str, token: str, ticket_channel: str, channel_user: str,
                           jlx_order_id: str, order_context: str = None) -> dict:
        """
        查询票号
        :param str path: 调用api接口的url后缀
        :param str method: 调用api的http请求方法
        :param str token: 调用api所需要的认证token
        :param str ticket_channel: 询价渠道，jlx:就旅行,bsp:bsp,qunarwn:蜗牛,qunarm:去哪儿M网,tongchengcg:同程分销,
                                   book51:51BOOK,hbgj:hbgj,b2b:b2b,b2c:b2c,yibao_b2b:易宝b2b,spider_b2b:自有自动B2B,
                                   spider_b2c:自有自动B2C,qunarApp:去哪APP,tdQunarApp:通达去哪APP,ctrip:携程,
                                   jlx_ctrip:自有携程,feizhum:飞猪M,tongchengapp:同程APP,ctripapp:携程APP,
                                   tongchenggift:同程礼品卡,jinghang:京杭,feizhuyd:飞猪永动,jegotrip:无忧行,
                                   spider_b2b_nopnr:自有白屏B2B,tcapp:同程APP熊大,ept:E票通B2B,czndc:南航NDC,
                                   jlx_tc_app:就旅行同程APP,meituan:美团分销,jlx_xc_app:就旅行携程APP
        :param str channel_user: 渠道用户
        :param str jlx_order_id: 就旅行订单id
        :param str order_context: 订单上下文
        :return:
        """
        headers = dict(Authorization=token)
        json = {
            "orderNo": jlx_order_id,
            "ticketChannel": ticket_channel,
            "ticketUser": {
                "name": channel_user
            }
        }
        if order_context:
            json['orderContext'] = order_context
        return self.__http_client.send_request(method=method, path=path, json=json, headers=headers)
