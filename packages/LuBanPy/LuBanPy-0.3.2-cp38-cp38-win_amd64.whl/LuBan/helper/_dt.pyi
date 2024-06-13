#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_dt.py
@Author     ：Alex
@Date       ：2024/1/17 18:14 
@Function   ：Dt组件 - 日期时间处理组件
"""
from typing import Union, Optional, List
import datetime


class Dt:
    # 返回一个以ISO-8601格式表示的日期和时间字符串
    # 参考：https://docs.python.org/zh-cn/3/library/datetime.html
    FMT_ISO: str = '_CALL_FUNCTION_ISO_FORMAT'

    # 本地化的适当日期和时间表示
    # 参考：https://docs.python.org/zh-cn/3/library/datetime.html#strftime-and-strptime-format-codes
    FMT_LOCALE: str = '%c'
    FMT_LOCAL_DATE: str = '%x'
    FMT_LOCAL_TIME: str = '%X'

    # 默认格式
    FMT_DEFAULT: str = '%Y-%m-%d %H:%M:%S'
    FMT_DATE: str = '%Y-%m-%d'
    FMT_TIME: str = '%H:%M:%S'

    __COUNTRY_CODES: Optional[List[str]] = None

    @classmethod
    def parse(cls, val, fmt: Optional[str] = None, tz: Union[str, int, datetime.tzinfo] = None) -> Optional[datetime.datetime]:
        """
        解释为datetime类型

        :param [str, int, float, datetime.datetime, datetime.date, time.struct_time] val:         需要解释的值
        :param Optional[str] fmt:                                               指字符串的时间格式
        :param tz:                                      指定时区信息
        :return Optional[datetime.datetime]:            解释成功，返回datetime对象，无法解释时返回None
        """
        pass

    @classmethod
    def format(cls, dt=None, fmt: Optional[str] = None) -> str:
        """
        > W3C - Date and Time Formats:  https://www.w3.org/TR/NOTE-datetime
        :param Optional[DateLike] dt:   指定datetime对象，如果为None时为当前时间
        :param str fmt:                 指定格式，默认格式%Y-%m-%d %H:%M:%S
        :return str:
        """
        pass


    @classmethod
    def getCountryCodes(cls) -> List[str]:
        """
        获取国家或地区国际代码

        :return:
        """
        pass

