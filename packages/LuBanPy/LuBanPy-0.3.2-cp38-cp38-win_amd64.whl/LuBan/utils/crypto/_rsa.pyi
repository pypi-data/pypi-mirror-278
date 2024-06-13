#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_rsa.py
@Author     ：Alex
@Date       ：2024/2/25 20:59 
@Function   ：RSA加密解密组件
"""
from Crypto.PublicKey.RSA import RsaKey
from typing import Union, Any, Tuple
from pathlib import Path
import _pickle as pickle


class RSAUtil:

    RSA_1024 = 1024
    RSA_2048 = 2048
    RSA_3072 = 3072
    RSA_4096 = 4096

    def __init__(self, publicKey: Union[str, Path, bytes, RsaKey] = None, privateKey: Union[str, Path, bytes, RsaKey] = None, encoding: str = 'utf-8'):
        """
        初始化方法

        :param Union[str, Path, bytes, RsaKey] publicKey:           设置公钥，[str,Path]为密钥文件路径，[bytes, RsaKey]为密钥
        :param Union[str, Path, bytes, RsaKey] privateKey:          设置私钥，[str,Path]为密钥文件路径，[bytes, RsaKey]为密钥
        :param str encoding:                                        设置编码，默认utf-8
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
        :raises:
            - TypeError
        """
        pass

    def encryptFile(self, infile: Union[str, Path], outfile: Union[str, Path] = None, force: bool = False) -> Union[bool, bytes]:
        """
        加密文件

        :param Union[str, Path] infile:             需要加密的文件
        :param Union[str, Path] outfile:            加密后输出的文件，可指定为目录名，当为None时返回加密后的bytes
        :param bool force:                          是否强制覆盖输出文件，默认值False
        :return Union[bool, bytes]:                 加密成功返回True，否则为False，如不设置输出文件时，返回bytes类型
        :raises:
            - AttributeError
            - FileNotFoundError
            - IsADirectoryError
            - FileExistsError
        """
        pass

    def decryptFile(self, infile: Union[str, Path], outfile: Union[str, Path] = None, force: bool = False) -> Union[bool, bytes]:
        """
        解密文件

        :param Union[str, Path] infile:             需要解密的文件
        :param Union[str, Path] outfile:            解密后输出的文件，可指定为目录名，当为None时返回加密后的bytes
        :param bool force:                          是否强制覆盖输出文件，默认值False
        :return Union[bool, bytes]:                 加密成功返回True，否则为False，如不设置输出文件时，返回bytes类型
        """
        pass

    def sign(self, data: Any) -> str:
        """
        使用私钥进行签名

        :param Any data:    明文数据，当为Path类型时获取文件签名
        :return str:        签名后的字符串
        :raises:
            - FileNotFoundError
            - IsADirectoryError
        """
        pass

    def verify(self, data: Any, sign: str) -> bool:
        """
        使用公钥验证签名

        :param Any data:        明文数据，当为Path类型时获取文件签名
        :param str sign:        签名的字符串
        :return bool:
        :raises:
            - FileNotFoundError
            - IsADirectoryError
        """
        pass

    @staticmethod
    def getBlockSize(key: RsaKey, encrypted: bool = True) -> int:
        """
        根据RsaKey获取块大小

        :param RsaKey key:              RsaKey对象实例
        :param bool encrypted:          解密时不需要要考虑预留位
        :return int:
        """
        pass

    @staticmethod
    def newkeys(bits: int = 1024) -> Tuple[RsaKey, RsaKey]:
        """
        生成新的私钥和公钥对

        :param int bits:            密钥长度
        :return (RsaKey, RsaKey):     返回 私钥和公钥对
        """
        pass

    @classmethod
    def dumps(cls, fname: Union[str, Path], key: Union[RsaKey, bytes]) -> bool:
        """
        密钥保存到文件

        :param Union[str, Path] fname:      指定保存的文件路径
        :param Union[RsaKey, bytes] key:    密钥对象（PEM格式）或数据
        :return bool:                       保存成功是返回True，否则返回False
        """
        pass

    @classmethod
    def loads(cls, fname: Union[str, Path]) -> Union[RsaKey, None]:
        """
        从文件读取密钥

        :param Union[str, Path] fname:      密钥文件路径
        :return Union[RsaKey, None]:        如果读取成功，返回RsaKey，否则返回None
        """
        pass

    @classmethod
    def importKey(cls, key: Union[str, Path, bytes, RsaKey]) -> Union[RsaKey, None]:
        """
        导入密钥，可以指定文件或字节

        :param Union[str, Path, bytes, RsaKey] key:
        :return RsaKey:
        """
        pass


