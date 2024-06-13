#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_env_manager.py
@Author     ：Alex
@Date       ：2024/2/23 20:55 
@Function   ：环境变量管理器
"""
import sys
from os import PathLike
from typing import Dict, Any, Optional
from pathlib import Path


class __EnvManager:

    @property
    def __LUBAN_DEBUG__(self) -> bool:
        """
        Luban框架专用调用阀
        :return:  默认返回False不开启
        """
        pass

    @property
    def __POSTFIX__(self) -> str:
        """获取环境变量名称私有变动态前缀"""
        pass

    @property
    def __BOOT_AT__(self) -> int:
        """获取应用启动时间"""
        pass

    @property
    def __IS_FROZEN__(self) -> bool:
        """
        应用是否已打包
        当前支持打包工具：
            - PyInstaller
        :return bool:
        """
        pass

    @property
    def __PROCESS_ID__(self) -> int:
        """获取当前进程ID"""
        pass

    @property
    def __PROCESS_NAME__(self) -> str:
        """获取当前进程名称"""
        pass

    @property
    def __PARENT_PROCESS_ID__(self) -> int:
        """获取父进程ID"""
        pass

    @property
    def __PARENT_PROCESS_NAME__(self) -> str:
        """获取父进程名称"""
        pass

    @property
    def __BOOT_PROCESS_ID__(self) -> int:
        """
        获取应用入口进程ID

        :return int:    返回启动主进程的ID
        """
        pass

    @property
    def __TOP_PROCESS_ID__(self) -> int:
        """
        获取主进程ID

        :return:    返回主进程ID
        """
        pass

    @property
    def __IS_TOP_PROCESS__(self) -> bool:
        """
        检查当前进程是否主进程

        :return bool:   当前是主进程返回True，否则返回False
        """
        pass

    @property
    def __RUNTIME_MODE__(self) -> int:
        """
        获取应用运行模式代码
            0 - 正常模式（单进程模式）
            1 - 应用模式（支持多进程）
        :return int:
        """
        pass

    def SET_APP_MODE(self, mode: bool):
        """
        设置APP运行模式
        :param bool mode:       True：启动APP模式，False停用APP模式
        :return:
        """
        pass

    @property
    def DEBUG(self) -> bool:
        """
        是否开启调试模式

        :return bool:
        """
        pass

    @DEBUG.setter
    def DEBUG(self, flag: bool):
        """
        动态设置调试模式
        :param flag:
        :return:
        """
        pass

    @property
    def PRODUCTION(self) -> bool:
        """
        是否生产环境

        :return bool:
        """
        pass

    @property
    def PROJECT_NAME(self) -> str:
        """
        项目名称，一般是英文，合法的文件名称
        :return str:
        """
        pass

    @property
    def APP_NAME(self) -> str:
        """
        获取应用名称
        :return str:
        """
        pass

    @property
    def VERSION(self) -> str:
        """
        获取应用版本号
        :return str:
        """
        pass

    @property
    def PYTHON_PATH(self) -> Path:
        """
        获取Python安装目录
        :return:
        """
        return Path(sys.executable).parent

    @property
    def ROOT_PATH(self) -> Path:
        """
        应用根目录
        :return:
        """
        pass

    @ROOT_PATH.setter
    def ROOT_PATH(self, path: PathLike):
        """
        设置新的ROOT_PATH路径

        :param PathLike path:       设置新的ROOT_PATH路径
        :return:
        """
        pass

    @property
    def SOURCE_PATH(self) -> Path:
        """
        源代码根目录，打包后为解包临时目录

        :return:
        """
        pass

    @property
    def PROJECT_PATH(self) -> Path:
        """
        项目主目录，默认与`SOURCE_PATH`一致，可修改，例如`src`

        :return:
        """
        pass

    @property
    def HOME_PATH(self) -> Path:
        """
        获取当前用户主目录
        :return:
        """
        pass

    @property
    def CONFIG_PATH(self) -> Path:
        """
        系统配置文件目录，建议与项目编译打包发布，可通过.env配置覆盖

        :return:
        """
        pass

    @property
    def RUNTIME_PATH(self) -> Path:
        """
        运行时目录（缓存、临时文件、日志等）
        :return Path:
        """
        pass

    @property
    def DATA_PATH(self) -> Path:
        """
        数据目录，一般存放数据库文件，例如sqlite，默认`runtime/data`目录

        :return:
        """
        pass

    @property
    def STORAGE_PATH(self) -> Path:
        """
        存储目录，一般是图片存放，默认`runtime/storage`目录

        :return:
        """
        pass

    @property
    def CACHE_PATH(self) -> Path:
        """
        缓存目录，默认`runtime/cache`目录

        :return:
        """
        pass

    @property
    def LOG_PATH(self) -> Path:
        """
        日志目录，默认`runtime/log`目录

        :return:
        """
        pass

    @property
    def TMP_PATH(self) -> Path:
        """
        临时目录，默认`runtime/tmp`目录

        :return:
        """
        pass

    def set(self, key: str, val):
        """
        设置环境变量项

        :param str key:     常量键名
        :param val:
        :return:
        """
        pass

    def get(self, key: str, default=None):
        """
        获取环境变量项

        :param key:
        :param default:
        :return:
        """
        pass

    def remove(self, key: str):
        """
        删除环境变量项

        :param key:
        :return:
        """
        pass

    def pop(self, key: str, default: None):
        """
        获取环境变量，并删除
        :param key:
        :param default:
        :return:
        """
        pass

    def clear(self):
        """
        清空全部自定义变量

        :return:
        """
        pass


    def reload(self, fname: Optional[PathLike] = None):
        """
        重新加载.env配置

        :param Optional[PathLike] fname:        可指定.env配置文件
        :return:
        """
        pass

    def loads(self, fname: PathLike) -> Optional[Dict[str, Any]]:
        """
        加载.env配置文件

        :param fname:           文件名
        :return:
        """
        pass

    def dumps(self, fIn: Optional[PathLike] = None, fOut: Optional[PathLike] = None) -> bool:
        """
        生成.env冻结

        :param fIn:         指定输入.env文件
        :param fOut:        指定输出frozen.env文件
        :return bool:       保存成功True，失败返回False
        """
        pass

    def makeVersionIncrement(self):
        """
        版本尾号自增长
        :return:
        """
        pass


Env = __EnvManager()

__all__ = ['Env']

