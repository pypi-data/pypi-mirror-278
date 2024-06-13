#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_hash.py
@Author     ：Alex
@Date       ：2024/1/17 17:30 
@Function   ：Hash - 组件：哈希计算辅助工具
"""
from typing import Union
from os import PathLike


class Hash:

    MD5 = 'md5'
    SHA1 = 'sha1'
    SHA224 = 'sha224'
    SHA256 = 'sha256'
    SHA384 = 'sha384'
    SHA512 = 'sha512'

    def __init__(self, hash_name: str, encoding: str = 'utf-8'):
        """
        hash对象实例构造器
        :param str hash_name:       指定哈希算法
        :param str encoding:        指定字符串编码
        """
        pass

    def update(self, data: Union[str, bytes]):
        """
        追加数据

        :param Union[str, bytes] data:
        :return Hash:       返回当前hash实例
        """
        pass

    def hexdigest(self) -> str:
        """
        返回哈希值

        :return str:
        """
        pass

    @classmethod
    def fileHash(cls, fpath: Union[str, PathLike], hash_name: str = 'sha1', chunk_size: int = -1) -> str:
        """
        计算文件哈希值

        :param Union[str, PathLike] fpath:           文件路径
        :param str hash_name:       指定哈希算法，默认为SHA-1
        :param int chunk_size:      分块读取文件
        :return str:
        """
        pass

    @classmethod
    def hash(cls, text: Union[str, bytes], hash_name: str, encoding: str = 'utf-8') -> str:
        """
        获取散列

        :param Union[str, bytes], text:     需要进行 hash 计算的 字符串或字节
        :param str hash_name:               指定 hash 名称，默认sha1
        :param str encoding:                指定字符串编码，默认utf-8
        :return str:
        """
        pass

    @classmethod
    def md5(cls, text: Union[str, bytes], encoding: str = 'utf-8') -> str:
        """
        计算字符串的 MD5 散列

        :param Union[str, bytes] text:      要进行md5散列的字符串或字节
        :param str encoding:                指定字符串编码类型，默认utf-8
        :return str:
        """
        pass

    @classmethod
    def sha1(cls, text: Union[str, bytes], encoding: str = 'utf-8') -> str:
        """
        计算字符串的 SHA-1 散列

        :param Union[str, bytes] text:      要进行散列计算的字符串或字节
        :param str encoding:                指定字符串编码类型，默认utf-8
        :return str:
        """
        pass

    @classmethod
    def sha224(cls, text: Union[str, bytes], encoding: str = 'utf-8') -> str:
        """
        计算字符串的 SHA-224 散列

        :param Union[str, bytes] text:      要进行散列计算的字符串或字节
        :param str encoding:                指定字符串编码类型，默认utf-8
        :return str:
        """
        pass

    @classmethod
    def sha256(cls, text: Union[str, bytes], encoding: str = 'utf-8') -> str:
        """
        计算字符串的 SHA-256 散列

        :param Union[str, bytes] text:      要进行散列计算的字符串或字节
        :param str encoding:                指定字符串编码类型，默认utf-8
        :return str:
        """
        pass

    @classmethod
    def sha384(cls, text: Union[str, bytes], encoding: str = 'utf-8') -> str:
        """
        计算字符串的 SHA-384 散列

        :param Union[str, bytes] text:      要进行散列计算的字符串或字节
        :param str encoding:                指定字符串编码类型，默认utf-8
        :return str:
        """
        pass

    @classmethod
    def sha512(cls, text: Union[str, bytes], encoding: str = 'utf-8') -> str:
        """
        计算字符串的 SHA-512 散列

        :param Union[str, bytes] text:      要进行散列计算的字符串或字节
        :param str encoding:                指定字符串编码类型，默认utf-8
        :return str:
        """
        pass

    @classmethod
    def blake2b(cls, text: Union[str, bytes], key: Union[str, bytes] = ..., salt: Union[str, bytes] = ...,
                person: Union[str, bytes] = ..., digest_size: int = -1, encoding: str = 'utf-8'):
        """
        BLAKE2 是在 RFC 7693 中定义的加密哈希函数，它有两种形式:
        - BLAKE2b，针对 64 位平台进行优化，并会生成长度介于 1 和 64 字节之间任意大小的摘要。
        - BLAKE2s，针对 8 至 32 位平台进行优化，并会生成长度介于 1 和 32 字节之间任意大小的摘要。
        BLAKE2 支持 keyed mode (HMAC 的更快速更简单的替代), salted hashing, personalization 和 tree hashing.

        :param Union[str, bytes] text:
        :param Union[str, bytes] key:
        :param Union[str, bytes] salt:
        :param Union[str, bytes] person:
        :param int digest_size:
        :param str encoding:
        :return:
        """
        pass



