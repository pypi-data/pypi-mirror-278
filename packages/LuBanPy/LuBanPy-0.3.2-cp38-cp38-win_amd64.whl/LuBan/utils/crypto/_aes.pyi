#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_aes.py
@Author     ：Alex
@Date       ：2024/2/25 20:59 
@Function   ：AES加密解密组件
"""
from typing import Union, Any
import _pickle as pickle
from Crypto.Cipher import AES as _AESCipher
from pathlib import Path


class AESUtil:

    # 加密方式
    MODE_CBC = _AESCipher.MODE_CBC
    MODE_ECB = _AESCipher.MODE_ECB

    # 填充类型
    NoPadding = ''
    ZeroPadding = ''
    PKCS5Padding = ''
    PKCS7Padding = ''

    def __init__(self, key: Union[str, bytes], mode: int = _AESCipher.MODE_ECB, iv: Union[str, bytes] = None, padding: str = 'PKCS7Padding', encoding: str = 'utf-8'):
        """
        初始化方法

        :param Union[str, bytes] key:       秘钥，字节型数据
        :param int mode:                    使用模式，只提供两种，AES.MODE_CBC，AES.MODE_ECB，默认AES.MODE_ECB
        :param Union[str, bytes] iv:        iv偏移量，字节型数据，当加密模式为CBC模式时必须设置
        :param str padding:                 填充模式，默认为PKCS7Padding, 可选NoPadding，ZeroPadding，PKCS5Padding，PKCS7Padding
        :param str encoding:                字符集编码，默认为utf-8
        """
        pass

    def encrypt(self, data: Any) -> Union[str, bytes, None]:
        """
        加密数据

        :param Any data:                        明文数据
        :return Union[str, bytes, None]:        根据来源数据类型返回结果
        """
        pass

    def decrypt(self, data: Union[str, bytes], unpack: bool = False) -> Any:
        """
        解密数据

        :param Union[str, bytes] data:          密文数据
        :param bool unpack:                     是否解包数据，默认值False
        :return Any:                            根据来源数据类型返回结果
        """
        pass

    def encryptFile(self, infile: Union[str, Path], outfile: Union[str, Path] = None, force: bool = False, chunk_size: int = 64 * 1024) -> Union[bool, bytes]:
        """
        加密文件

        :param Union[str, Path] infile:             需要加密的文件
        :param Union[str, Path] outfile:            加密后输出的文件，可指定为目录名，当为None时返回加密后的bytes
        :param bool force:                          是否强制覆盖输出文件，默认值False
        :param int chunk_size:                      分块读取文件大小
        :return Union[bool, bytes]:                 加密成功返回True，否则为False，如不设置输出文件时，返回bytes类型
        """
        pass

    def decryptFile(self, infile: Union[str, Path], outfile: Union[str, Path] = None, force: bool = False, chunk_size:int = 64 * 1024) -> Union[bool, bytes]:
        """
        解密文件

        :param Union[str, Path] infile:             需要解密的文件
        :param Union[str, Path] outfile:            解密后输出的文件，可指定为目录名，当为None时返回加密后的bytes
        :param bool force:                          是否强制覆盖输出文件，默认值False
        :param int chunk_size:                      分块读取文件大小
        :return Union[bool, bytes]:                 加密成功返回True，否则为False，如不设置输出文件时，返回bytes类型
        """
        pass


