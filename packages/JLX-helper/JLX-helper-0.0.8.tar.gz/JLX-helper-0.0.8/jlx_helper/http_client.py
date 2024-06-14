# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  JLX-helper
# FileName:     http_client.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/06/07
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import requests
from json import dumps
from copy import deepcopy
from jlx_helper.libs import logger
from jlx_helper.utils import covert_dict_key_to_lower, get_html_title


class HttpService(object):
    __url = None
    __domain = None
    __time_out = 120
    __protocol = None
    __headers: dict = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " +
                      "Chrome/123.0.0.0 Safari/537.36"
    }

    def __init__(self, domain: str, protocol: str) -> None:
        self.__domain = domain
        self.__protocol = protocol

    def send_request(self, method: str, path: str, params: dict = None, data: dict = None, json: dict = None,
                     headers: dict = None) -> dict:
        if headers and isinstance(headers, dict):
            __headers = deepcopy(self.__headers)
            __headers.update(headers)
        else:
            __headers = self.__headers
        self.__url = "{}://{}{}".format(self.__protocol, self.__domain, path)
        # 发送HTTP请求
        logger.debug(
            "发起http请求，url: {}, 方法：{}，请求params参数：{}，请求headers参数：{}，请求data参数：{}，请求json参数：{}".format(
                self.__url,
                method,
                dumps(params) if params else "{}",
                dumps(__headers),
                dumps(data) if data else "{}",
                dumps(json) if json else "{}"
            )
        )
        return self.__send_http_request(
            method=method, params=params, data=data, json=json, url=self.__url, time_out=self.__time_out,
            headers=__headers
        )

    @classmethod
    def __send_http_request(cls, url: str, method: str, time_out: int, headers: dict = None, params: dict = None,
                            data: dict = None, json: dict = None) -> dict:
        # 实际发送HTTP请求的内部方法
        # 使用 requests 库发送请求
        method = method.lower().strip()
        if method in ("get", "post"):
            try:
                if method == "get":
                    response = requests.get(url, params=params, verify=False, timeout=time_out, headers=headers)
                else:
                    response = requests.post(
                        url, params=params, json=json, data=data, verify=False, timeout=time_out, headers=headers
                    )
                result = cls.__parse_data_response(url=url, response=response)
            except Exception as e:
                logger.error("调用url<{}>异常，原因：{}".format(url, str(e)))
                result = dict(code=500, message=str(e), data=dict())
        else:
            result = dict(code=400, message="Unsupported HTTP method: {}".format(method), data=dict())
        return result

    @classmethod
    def __parse_data_response(cls, url: str, response: requests.Response) -> dict:
        # 获取 Content-Type 头信息
        content_type = response.headers.get('Content-Type')
        # 判断返回的内容类型
        if 'application/json' in content_type or 'text/json' in content_type:
            # JSON 类型
            data = covert_dict_key_to_lower(d=response.json())
        elif 'text/plain' in content_type:
            # 纯文本类型
            data = dict(code=response.status_code, message=get_html_title(
                html=response.text), data=response.text)
        else:
            # 其他类型，默认视为二进制内容
            content = response.content.decode('utf-8')
            data = dict(code=response.status_code,
                        message=get_html_title(html=content), data=content)
        logger.debug("调用url: {} 的正常返回值为：{}".format(url, dumps(data)))
        return data
