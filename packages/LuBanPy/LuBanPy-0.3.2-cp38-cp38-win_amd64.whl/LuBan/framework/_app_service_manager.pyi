#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_app_service_manager.py
@Author     ：Alex
@Date       ：2024/2/26 10:52 
@Function   ：应用服务管理器
"""
from typing import Optional


class __AppServiceManager:

    HOOK_INIT = 'init'
    HOOK_READY = 'ready'
    HOOK_EXIT = 'exit'

    def __init__(self):
        """
        初始化函数
        """
        pass

    @property
    def isDebug(self) -> bool:
        pass

    @property
    def isProduction(self) -> bool:
        pass

    def run(self, loop: bool = True):
        """
        应用服务管理器运行正在启动入口

        :param bool loop:       是否启用主系统消息
        :return:
        """
        pass

    def exit(self):
        """
        退出应用操作(推送请求)
        :return:
        """
        pass

    @property
    def isExit(self) -> bool:
        """当前是否已标记退出"""
        pass

    def command(self, directive: str, params=None):
        """
        发送命令
        :param directive:
        :param params:
        :return:
        """
        pass

    def set(self, key: str, val):
        """
        设置全局变量
        :param key:
        :param val:
        :return:
        """
        pass

    def get(self, key: str, default=None):
        """
        获取全局变量
        :param key:
        :param default:
        :return:
        """
        pass

    def pop(self, key: str, default=None):
        """
        获取全局变量，并删除
        :param key:
        :param default:
        :return:
        """
        pass

    def remove(self, key: str):
        """
        删除全局变量
        :param key:
        :return:
        """
        pass

    def send(self, msg, receiver=None):
        """
        发送消息

        :param msg:
        :param receiver:
        :return:
        """
        pass

    def start(self, cls: str, params: Optional[dict] = None, name: Optional[str] = None, daemon: bool = False, worker: int = 1, sync: bool = False):
        """
        启动新的服务进程发送指令

        :param str cls:                         应用服务类名，需要实现`AppServiceInterface`接口
        :param Optional[dict] params:           可以给应用服务类传递参数
        :param Optional[str] name:              指定应用服务的名称，未指定时使用类名
        :param bool daemon:                     是守护进程
        :param int worker:                      指定服务启动的子进程数量，最少必须为1
        :param sync sync:                       是否使用同步(True)或异步(False)模式启动进程（异步无需等待进程启动完成，即可调用下一进程启动）
        :return:
        """
        pass


App = __AppServiceManager()

__all__ = ['App']


