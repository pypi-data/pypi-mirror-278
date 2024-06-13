#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：build2_ext.py
@Author     ：Alex
@Date       ：2024/5/26 19:30 
@Function   ：使用Cython项目编译为.pyd或.so
"""
from typing import Iterable, Union, Set
from os import PathLike
from pathlib import Path


class Build2EXT:


    def __init__(self,
                 modules: Union[str, Iterable[str], Iterable[PathLike]],
                 excludes: Union[str, Iterable[str]] = (),
                 build_dir: Union[PathLike, str, Path] = 'build',
                 out_dir: Union[PathLike, str, Path, None] = None,
                 project_root: Union[PathLike, str, Path, None] = None):
        """
        初始化方法

        :param modules:         指定模块列表，可以模块名或文件名
        :param excludes:        需要排除的模块
        :param build_dir:       c代码生成构建目录，默认build
        :param out_dir:         生成到输出到当前目录，默认None为当前相同目录(inplace=True)
        :param project_root:    项目根目录
        """
        pass

    def findModuleFiles(self) -> Set[Path]:
        """
        收集模块或包的所有文件

        :return:
        """
        pass

    def clean(self):
        """
        清空编译，包括c、pyd文件

        :return:
        """
        pass

    def run(self, force: bool = True):
        """
        运行编译
        编译生成pyd、so扩展

        :param force:       是否自动清空已生成的文件
        :return:
        """
        pass


