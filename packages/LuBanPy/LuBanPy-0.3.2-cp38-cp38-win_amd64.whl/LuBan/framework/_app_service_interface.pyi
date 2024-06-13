#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_app_service_interface.py
@Author     ：Alex
@Date       ：2024/2/26 12:22 
@Function   ：应用服务接口
"""
from abc import abstractmethod


class AppServiceInterface:


    @property
    def __CURRENT_PROCESS_SERVICE_NO__(self) -> 0:
        pass

    def onInit(self):
        """
        应用服务初始化接口
        :return:
        """
        pass

    @abstractmethod
    def run(self):
        """
        应用服务实现入口
        :return:
        """
        # print("[%s] %s.%s - 应用服务实现入口" % (datetime.datetime.now(), self.__class__.__name__, sys._getframe().f_code.co_name))
        pass

    def onDone(self):
        """
        应用服务执行完成接口
        :return:
        """
        pass

    def onExit(self):
        """
        接收到请求退出应用信号
        :return:
        """
        pass

    def onReceive(self, sender, receiver, msg):
        """
        消息监听接口

        :param sender:
        :param receiver:
        :param msg:
        :return:
        """
        pass

