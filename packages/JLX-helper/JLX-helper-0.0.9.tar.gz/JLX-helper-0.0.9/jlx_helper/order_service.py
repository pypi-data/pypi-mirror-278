# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  JLX-helper
# FileName:     order_service.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/06/07
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from json import dumps
from jlx_helper.api import JLXApi
from jlx_helper.libs import logger
from jlx_helper.config import url_map, card_type_map, age_type_map
from jlx_helper.utils import timestamp_to_datetime_str, get_age, get_gender_code


class OrderService(object):

    def __init__(self, user: str = None, password: str = None):
        self.__user = user or url_map.get("auth_username")
        self.__password = password or url_map.get("auth_password")
        self.__client = JLXApi(domain=url_map.get("domain"), protocol=url_map.get("procotol"))

    @property
    def user(self):
        return self.__user

    def get_token(self) -> str:
        response_data = self.__client.get_authorization_token(
            method="post", path=url_map.get("get_authorization_token"), user=self.__user, password=self.__password
        )
        token = ""
        if response_data.get("code") == 0 and response_data.get("success") is True:
            token = response_data.get("data").get("token")
            expire_time = response_data.get("data").get("expireTime")
            expire_time_str = timestamp_to_datetime_str(timestamp=expire_time)
            logger.debug("获取就旅行api鉴权token值：{}，有效期至：{}".format(token, expire_time_str))
        else:
            logger.warning("获取就旅行api鉴权token失败，接口返回内容：{}".format(dumps(response_data)))
        return token

    def get_flight_quotation(self, ticket_channel: str, channel_user: str, channel_password: str, departure_date: str,
                             departure_city_code: str, arrive_city_code: str, flight_no: str, cabin: str = None,
                             channel_token: str = None, jlx_token: str = None, product_type: str = 'cpa',
                             trip_type: str = 'single_trip') -> dict:
        if not jlx_token:
            jlx_token = self.get_token()
            if not jlx_token:
                return dict()
        response_data = self.__client.get_query_quotation(
            method="post", path=url_map.get("get_query_quotation"), token=jlx_token, ticket_channel=ticket_channel,
            channel_user=channel_user, channel_password=channel_password, departure_city_code=departure_city_code,
            arrive_city_code=arrive_city_code, departure_date=departure_date, flight_no=flight_no, cabin=cabin,
            channel_token=channel_token, product_type=product_type, trip_type=trip_type
        )
        if response_data.get("code") == 0 and response_data.get("success") is True:
            return dict(
                ticket_channel=ticket_channel, channel_user=channel_user, channel_password=channel_password,
                departure_date=departure_date, departure_city_code=departure_city_code, flight_no=flight_no,
                arrive_city_code=arrive_city_code, cabin=cabin, channel_token=channel_token, product_type=product_type,
                trip_type=trip_type, quotation_result=response_data.get("data")) if isinstance(
                response_data.get("data"), list
            ) and len(response_data.get("data")) > 0 else dict()
        else:
            logger.warning("获取就旅行航班报价信息失败，接口返回内容：{}".format(dumps(response_data)))
        return dict()

    def gen_jlx_order(self, ticket_channel: str, channel_user: str, order_id: str, departure_date: str,
                      departure_city_code: str, arrive_city_code: str, flight_no: str, passengers: list,
                      internal_phone: str, internal_contact: str, cabin: str = None, jlx_token: str = None,
                      price_context: str = None, conditions: list = None, trip_type: str = 'single_trip') -> dict:
        if not jlx_token:
            jlx_token = self.get_token()
            if not jlx_token:
                return dict()
        passengers = [{
            "passageName": x.get("passenger"), "cardType": card_type_map.get(x.get("card_type")),
            "cardNo": x.get("card_id"), "ageType": age_type_map.get(x.get("passenger_type")),
            "age": x.get("age") or get_age(birth_date=x.get("birth_day"), card_id=x.get("card_id")),
            "gender": get_gender_code(gender=x.get("gender")), "nationality": x.get("nationality"),
            "cardExpired": x.get("card_expired"), "cardIssuePlace": x.get("card_issue_place"),
            "birthDay": x.get("birth_day"), "phone": x.get("mobile")
        } for x in passengers]
        response_data = self.__client.gen_service_order(
            method="post", path=url_map.get("gen_service_order"), token=jlx_token, ticket_channel=ticket_channel,
            channel_user=channel_user, order_id=order_id, departure_city_code=departure_city_code,
            arrive_city_code=arrive_city_code, departure_date=departure_date, flight_no=flight_no,
            passengers=passengers, internal_phone=internal_phone, price_context=price_context, conditions=conditions,
            cabin=cabin, trip_type=trip_type, internal_contact=internal_contact
        )
        if response_data.get("code") == 0 and response_data.get("success") is True:
            return dict(
                order_id=response_data.get("data").get("orderNo"), price=response_data.get("data").get("price"),
                order_context=response_data.get("data").get("orderContext"),
                raw_order_id=response_data.get("data").get("yourOrderNo"),
            )
        else:
            logger.warning("创建就旅行出票订单失败，接口返回内容：{}".format(dumps(response_data)))
        return dict()

    def payment_jlx_order(self, ticket_channel: str, channel_user: str, jlx_order_id: str, pay_type: str,
                          jlx_token: str = None, bank_card_info: dict = None, pay_user_info: dict = None) -> dict:
        if not jlx_token:
            jlx_token = self.get_token()
            if not jlx_token:
                return dict()
        response_data = self.__client.payment_service_order(
            method="post", path=url_map.get("payment_service_order"), token=jlx_token, ticket_channel=ticket_channel,
            channel_user=channel_user, jlx_order_id=jlx_order_id, pay_type=pay_type, bank_card_info=bank_card_info,
            pay_user_info=pay_user_info
        )
        if response_data.get("code") == 0 and response_data.get("success") is True:
            # 0出票中，1出票完成，2出票失败
            return dict(
                jlx_order_id=response_data.get("data").get("orderNo"), price=response_data.get("data").get("price"),
                order_context=response_data.get("data").get("orderContext"),
                status=response_data.get("data").get("status"), bill_id=response_data.get("data").get("billNo"),
            )
        else:
            logger.warning("支付就旅行订单<{}>失败，接口返回内容：{}".format(jlx_order_id, dumps(response_data)))
        return dict()

    def get_jlx_order_itinerary_info(self, ticket_channel: str, channel_user: str, jlx_order_id: str,
                                     jlx_token: str = None, order_context: str = None) -> dict:
        if not jlx_token:
            jlx_token = self.get_token()
            if not jlx_token:
                return dict()
        response_data = self.__client.get_itinerary_info(
            method="post", path=url_map.get("payment_service_order"), token=jlx_token, ticket_channel=ticket_channel,
            channel_user=channel_user, jlx_order_id=jlx_order_id, order_context=order_context
        )
        if response_data.get("code") == 0 and response_data.get("success") is True:
            # 0出票中，1出票完成，2出票失败
            return dict(
                jlx_order_id=response_data.get("data").get("orderNo"),
                error_msg=response_data.get("data").get("errorMsg"), status=response_data.get("data").get("status"),
                tickets=response_data.get("data").get("tickets") if isinstance(
                    response_data.get("data"), list) else list(),
            )
        else:
            logger.warning("获取就旅行订单<{}>的票号失败，接口返回内容：{}".format(jlx_order_id, dumps(response_data)))
        return dict()


if __name__ == "__main__":
    ser = OrderService()
    t = ser.get_token()
    logger.info(t)
