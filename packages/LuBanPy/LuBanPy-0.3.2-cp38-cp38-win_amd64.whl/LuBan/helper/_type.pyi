#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：Yay 
@File       ：_type.py
@Author     ：Alex
@Date       ：2023/4/22 18:49 
@Function   ：类型相关辅助工具套件
"""


class Type:

    @classmethod
    def isNull(cls, obj) -> bool:
        """
        检查对象是否为Null未定义对象

        :param obj:
        :return:
        """
        pass

    @classmethod
    def empty(cls, obj) -> bool:
        """
        检查对象是否为空

        :param obj:
        :return :
        """
        pass

    @classmethod
    def equal(cls, obj1, obj2) -> bool:
        """
        判断两个对象是否相等

        :param obj1:
        :param obj2:
        :return bool:
        """
        pass

    @classmethod
    def isHashable(cls, obj) -> bool:
        """
        检查对象是否可以返回hash值

        :param obj:     测试对象
        :return bool:
        """
        pass

    @classmethod
    def isCallable(cls, obj) -> bool:
        """
        检查obj是否可调用

        :param obj:
        :return bool:
        """
        pass
    @classmethod
    def isIterable(cls, obj) -> bool:
        """
        检查对象是否可迭代，对str标注为非可迭代类型

        :param obj:
        :return bool:
        """
        pass

    @classmethod
    def existsMethod(cls, obj, method: str) -> bool:
        """
        是否存在方法
        :param obj:     类或实例
        :param method:  方法名
        :return:
        """
        pass


