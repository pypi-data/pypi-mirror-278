#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：build2_exe.py
@Author     ：Alex
@Date       ：2024/6/5 22:28 
@Function   ：使用PyInstaller构建生成可执程序
"""
from typing import Union, Iterable, Optional, Set
from pathlib import Path
from os import PathLike


class Build2EXE:



    def __init__(self,
                 entry: Union[str, Path, PathLike],
                 name: Optional[str] = None,
                 modules: Union[str, Iterable[str], None] = None,
                 excludes: Union[str, Iterable[str]] = (),
                 onefile: bool = False,
                 console: bool = True,
                 frozen: bool = True,
                 project_root: Union[PathLike, str, Path, None] = None):
        """
        初始化方法

        :param entry:           程序入口script文件名
        :param name:            指定项目（产生的 spec）名字。如果省略该选项，那么第一个脚本的主文件名将作为 spec 的名字
        :param modules:         指定需要打包的模块（不需要.py后缀）名包
        :param excludes:        （可选）指定需要排除的目录规则
        :param onefile:         是否产生单个可执行文件或目录（包含多个文件）
        :param console:         指定使用命令行窗口运行程序（仅对 Windows 有效）
        :param frozen:          是否冻结.env和config配置，默认True
        :param project_root:    指定项目根目录
        """
        pass

    def icon(self, icon: Union[str, Path, PathLike]):
        """
        设置图标文件
        :param icon:
        :return:
        """
        return self

    def data(self, data: dict):
        """
        打包额外资源

        :param dict data:   打包额外资源，key源目录，val为目标目录
        :return:
        """
        return self

    def binary(self, binary: dict):
        """
        打包额外的代码，与–add-data不同的是，用binary添加的文件，pyi会分析它引用的文件并把它们一同添加进来

        :param dict binary:
        :return:
        """
        return self

    def excludeModules(self, excludes: Union[str, Iterable[str]]):
        """
        添加需要排除的包名

        :param Union[str, Iterable[str]] excludes:       需要排序的模块名称（非文件路径）
        :return:
        """
        return self

    def hiddenImports(self, hiddens: Union[str, Iterable[str]]):
        """
        设置–hidden-import

        :param Union[str, Iterable[str]] hiddens:
        :return:
        """
        return self

    def upx(self, upx: Union[str, Path, bool] = True):
        """
        upx设置

        :param Union[str, Path, bool] upx:  True尽量使用upx，False强制不使用，字符串或路径时指定upx目录
        :return:
        """
        return self

    def frozen(self, frozen: bool = True):
        """
        冻结环境变量及配置

        :param frozen:      是否冻结.env和config配置，默认True
        :return:
        """
        return self

    def findUserModules(self) -> Set[str]:
        """
        返回用户模块集合
        :return:
        """
        pass

    def findModuleRequires(self) -> Set[str]:
        """
        收集项目的模块依赖
        :return:
        """
        pass

    def clean(self, force: bool = False):
        """
        清空打包构建生成的文件

        :param force:       删除已存在的dist包
        :return:
        """
        pass

    def run(self, force: bool = True, compiled: bool = True, autoClean: bool = True):
        """
        运行打包构建

        :param bool force:              如果dist文件夹内已经存在生成文件，则不询问用户，直接覆盖
        :param bool compiled:           项目是否需要使用Cython进行编译
        :param bool autoClean:          构建完成后，是否自动清空临时文件
        :return:
        """
        pass

