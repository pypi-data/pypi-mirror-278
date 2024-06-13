#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_file.py
@Author     ：Alex
@Date       ：2024/2/25 19:33 
@Function   ：File - 组件：文件相关辅助工具
"""
from os import PathLike
from pathlib import Path
from typing import List, Union


class File:

    @staticmethod
    def isBinary(fpath: PathLike) -> bool:
        """
        是否二进制文件（非文本）

        :param fpath:       文件名称
        :return bool:
        """
        pass

    @staticmethod
    def isText(fpath: PathLike) -> bool:
        """
        是否文本文件
        :param fpath:
        :return bool:
        """
        pass

    @classmethod
    def listdir(cls, fpath: Union[str, Path] = ..., pattern: str = '*', recursive: bool = False) -> List[Path]:
        """
        列出匹配的文件或目录

        :param Union[str, Path] fpath:      获取指定目录文件和文夹列表
        :param str pattern:
        :param bool recursive:              递归
        :return List[Path]:
        """
        pass





