#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_pkg.py
@Author     ：Alex
@Date       ：2024/3/11 16:09 
@Function   ：Pkg包管理工具套件
"""
from pathlib import Path
from os import PathLike
from typing import Union, Optional, List, Tuple, Set, Dict, Iterable
import contextlib


@contextlib.contextmanager
def _keep_sys_modules_clean():
    pass


class PkgUtil:

    keep_sys_modules_clean = _keep_sys_modules_clean

    @staticmethod
    def importFrom(module: str, locals: Optional[dict] = None):
        """
        通过字符串导入模块

        :param str module:
                - 模块名
                - 包名
                - 类路径
        :param locals:
        :return:
        """
        pass

    @staticmethod
    def getProjectRoot(project_root: Union[PathLike, Path, str, None] = None) -> Path:
        """
        获取项目根目录
        :param Union[PathLike, Path, str, None] project_root:     指定项目根目录，默认使用环境变量PROJECT_PATH值
        :return:
        """
        pass

    @staticmethod
    def checkStdLib(name: str) -> bool:
        """
        检查是否标准（系统内置）模块
        :param name:
        :return:
        """
        pass

    @classmethod
    def isUserModule(cls, module: str, project_root: Union[PathLike, Path, str, None] = None) -> bool:
        """
        是否自定义模块

        :param module:
        :param project_root:        指定项目根目录，默认使用环境变量PROJECT_PATH值
        :return:
        """
        pass

    @classmethod
    def parseFileImports(cls, fname: Union[str, Path, PathLike], project_root: Union[PathLike, Path, str, None] = None) -> List[str]:
        """
        分析文件的import项

        识别格式：
            import a
            import a,b
            from a import a
            from a import a,b
            from a import (a,...可换行...,b)
            from a.b import c
            from Luban.helper import *
        :param fname:       支持.py或.ipynb类型文件
        :param project_root:        代码指定项目根目录
        :return:
        """
        pass

    @classmethod
    def getModuleFile(cls, module: str, project_root: Union[PathLike, Path, str, None] = None) -> Optional[Path]:
        """
        通过模块名称获取模块文件/目录
        :param module:      模块名称
        :param project_root:    指定工程目录
        :return:
        """
        pass

    @classmethod
    def collectModuleFiles(cls, module: Union[str, Path, PathLike], excludes: Union[str, Iterable[str]] = (), recursive: bool = True, project_root: Union[PathLike, Path, str, None] = None) -> List[Path]:
        """
        收集模块的文件
        :param module:      模块名
                        - 包名（获取包所在目录）
                        - 模块名（自动转换为.py文件路径）
                        - 文件或目录
        :param excludes:     排除
        :param recursive:   递归
        :param project_root:        指定项目根目录，默认为
        :return:
        """
        pass

    @classmethod
    def collectImports(cls,
                       modules: Union[str, List[str], Tuple[str], Set[str], None] = None,
                       excludes: Union[str, List[str], Tuple[str], Set[str], None] = None,
                       onlyParseUserModel: bool = True,
                       project_root: Union[PathLike, Path, str, None] = None) -> List[str]:
        """
        收集项目的导入项（不包括内置模块）
        :param Union[str, List[str], Tuple[str], Set[str], None] modules:     （可选）指定需要收集的模块列表
        :param Union[str, List[str], Tuple[str], Set[str], None] excludes:     （可选）指定需要排除的目录
        :param bool onlyParseUserModel:     （可选）是否只分析用户自定义模块，默认是
        :param Union[PathLike, Path, str, None] project_root:               （可选）指定项目根目录
        :return:
        """
        pass

    @classmethod
    def collectDependencies(cls,
                            modules: Union[str, List[str], Tuple[str], Set[str], None] = None,
                            excludes: Union[str, List[str], Tuple[str], Set[str], None] = None,
                            project_root: Union[PathLike, Path, str, None] = None) -> Dict[str, Dict[str, str]]:
        """
        收集项目依赖

        :param Union[str, List[str], Tuple[str], Set[str], None] modules:     （可选）指定需要收集的模块列表
        :param Union[str, List[str], Tuple[str], Set[str], None] excludes:     （可选）指定需要排除的目录
        :param Union[PathLike, Path, str, None] project_root:               （可选）指定项目根目录
        :return:
        """
        pass
