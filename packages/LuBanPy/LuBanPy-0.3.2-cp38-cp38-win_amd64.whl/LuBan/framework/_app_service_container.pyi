#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_app_service_container.py
@Author     ：Alex
@Date       ：2024/2/27 21:22 
@Function   ：应用服务进程容器
"""
import multiprocessing


class _AppServiceProcessWrap:

    @classmethod
    def run(
            cls,
            _PNO, _PPNO,
            serviceCls, params,
            mainQ: multiprocessing.Queue,
            serviceQ: multiprocessing.Queue,
            appVars, appLock,
            envVars, envLock,
            configVars, configLock,
            syncLock
        ):
        """服务子进程业务处理"""
        pass


class AppServiceContainer:

    def __init__(self, _ppno: int, _pno: int, mainQ: multiprocessing.Queue, **kwargs):
        """
        初始化应用服务容器

        :param int _ppno:                       上级服务进程序号
        :param int _pno:                        当前分配服务进程序号
        :param mainQ: multiprocessing.Queue     系统消息总线队列
        :param str cls:                         应用服务类名，需要实现`AppServiceInterface`接口
        :param Optional[dict] params:           可以给应用服务类传递参数
        :param Optional[str] name:              指定应用服务的名称，未指定时使用类名
        :param bool daemon:                     是守护进程
        :param int worker:                      指定服务启动的子进程数量，最少必须为1
        :param sync sync:                       是否使用同步(True)或异步(False)模式启动进程（异步无需等待进程启动完成，即可调用下一进程启动）
        """
        pass

    @property
    def __CURRENT_PROCESS_NO__(self) -> int:
        """应用服务进程序号"""
        pass

    @property
    def __CURRENT_PPROCESS_NO__(self) -> int:
        """应用服务进程父序号"""
        pass

    @property
    def name(self) -> str:
        """获取应用服务名称"""
        pass

    @property
    def __CURRENT_PROCESS_ID__(self) -> int:
        """应用服务进程ID"""
        pass

    def exit(self):
        """调用退出请求操作"""
        pass

    def start(self, appVars, appLock, envVars, envLock, configVars, configLock):
        """
        启动应用服务

        :param appVars:         全局共享变量
        :param appLock:         全局共享进程锁
        :param envVars:         环境变量VARS共享变量
        :param envLock:         环境变量进程锁
        :param configVars:      配置共享变量
        :param configLock:      配置共享进程锁
        :return:
        """
        pass

    def lockSync(self):
        pass

    def unlockSync(self):
        pass

    def receiveIPCMsg(self, sender, receiver, msg):
        """
        接收IPC消息

        :param sender:      发送者
        :param receiver:    接收者
        :param msg:         消息
        :return:
        """
        pass

