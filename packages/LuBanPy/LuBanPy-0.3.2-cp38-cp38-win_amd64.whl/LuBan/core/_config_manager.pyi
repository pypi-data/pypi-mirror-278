#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_config_manager.py
@Author     ：Alex
@Date       ：2024/2/28 12:34 
@Function   ：配置管理器
"""
from typing import Optional, Any


class __ConfigManager:


    def get(self, key: Optional[str] = None, default: Any = None):
        """
        获取配置项，可以使用 “点” 语法访问配置值

        :param Optional[str] key:       键名，如不设置，返回全部配置项
        :param Any default:             键不存在时返回该值
        :return:
        """
        pass

    def set(self, key: str, val):
        """
        设置配置项值

        :param str key: 键名，可以使用 “点” 语法设置。
        :param val:
        :return:
        """
        pass

    def has(self, key: str) -> bool:
        """
        判断是否有配置项，

        :param str key:   键名， 可以使用 “点” 语法设置。
        :return:
        """
        pass

    def pop(self, key: str, default=None):
        """
        获取配置项，并删除
        :param str key:     键名， 可以使用 “点” 语法设置。
        :param default:     默认值
        :return:
        """
        pass

    def remove(self, key: str):
        """
        删除配置项

        :param str key:     键名， 可以使用 “点” 语法设置。
        :return:
        """
        pass

    def reload(self):
        """
        重新载入配置
        自动加载`CONFIG_PATH`目录下的全部配置
        :return:
        """
        pass

    @staticmethod
    def loads(force: bool = False):
        """
        从文件载入配置项

        :param bool force:          是否强制加载，默认为False，开发模式加载.py源文件，打包模式只加载.frozen
        :return:
        """
        pass


Config = __ConfigManager()

__all__ = ['Config']

