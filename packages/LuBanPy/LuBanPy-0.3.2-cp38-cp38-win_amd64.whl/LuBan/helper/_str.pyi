#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_str.py
@Author     ：Alex
@Date       ：2024/1/8 19:38 
@Function   ：字符串相关
"""
import re
from typing import Optional, Union, Tuple, List, Set, Dict, Callable, Any


class Str:

    CHAR_TYPE_DIGITS = 0  # 纯数字
    CHAR_TYPE_ALPHA = 1  # 纯字母
    CHAR_TYPE_ALPHA_NUM = 2  # 字母和数字
    CHAR_TYPE_ALPHA_DASH = 3  # 字母、数字、下划线，中划线
    CHAR_TYPE_ALPHA_CHS = 4  # 中文

    @classmethod
    def random(cls, length: int = 32, charType: int = 1, expand: str = '') -> str:
        """
        生成指定长度的随机字母数字组合的字符串

        :param int length:      生成字符串长度
        :param int charType:    字符串组成类型，
        :param str expand:      （可选）自定义扩展字符串
        :return:
        """
        pass

    @staticmethod
    def isEmpty(val, trim: bool = False) -> bool:
        """
        确定给定的字符串是否为空

        :param val:         字符串值
        :param bool trim:   是否去除前向空格
        :return bool:
        """
        pass

    @staticmethod
    def isNotEmpty(val, trim: bool = False) -> bool:
        """
        确定给定的字符串是否不为空

        :param val:         字符串值
        :param bool trim:   是否去除前向空格
        :return bool:
        """
        pass

    @classmethod
    def default(cls, *args, default: Optional[str] = None, trim: bool = True) -> Optional[str]:
        """
        返回首个非空字符串
        :param args:        按顺序检查返回首个非空字符串
        :param default:     默认值
        :param trim:        检查时是否去除前向空格
        :return:
        """
        pass

    @staticmethod
    def ascii(value: str, language: str = 'en') -> str:
        """
        TODO：尝试将字符串转换为 ASCII 值

        :param value:
        :param language:
        :return:
        """
        pass

    @staticmethod
    def after(subject: str, search: str) -> str:
        """
        返回字符串中指定值之后的所有内容

        :param str subject:
        :param str search:
        :return str:
        """
        pass

    @classmethod
    def afterLast(cls, subject: str, search: str) -> str:
        """
        返回字符串中指定值最后一次出现后的所有内容

        :param str subject:
        :param str search:
        :return:
        """
        pass

    @classmethod
    def before(cls, subject: str, search: str) -> str:
        """
        方法返回字符串中给定值之前的所有内容

        :param str subject:
        :param str search:
        :return:
        """
        pass

    @classmethod
    def beforeLast(cls, subject: str, search: str):
        """
        返回字符串中指定值最后一次出现前的所有内容

        :param str subject:
        :param str search:
        :return:
        """
        pass

    @classmethod
    def between(cls, subject: str, start: str, end: str) -> str:
        """
        返回字符串在指定两个值之间的内容

        :param str subject:     字符串
        :param str start:       起始字符串
        :param str end:         结束字符串
        :return str:
        """
        pass

    @classmethod
    def betweenFirst(cls, subject: str, start: str, end: str) -> str:
        """
        返回字符串在指定两个值之间的最小可能的部分

        :param str subject:     字符串
        :param str start:       起始字符串
        :param str end:         结束字符串
        :return str:
        """
        pass

    @staticmethod
    def find(text: str, search: str, caseSensitive: bool = True) -> int:
        """
        获取子字符串在字符串的首次出现位置

        :param str text:            要被检查的 string
        :param str search:          在 text 中查找这个字符串。
        :param bool caseSensitive:  是否大写小敏感，默认为True
        :return int:    如果是返回开始的索引值，否则返回-1
        """
        pass

    @staticmethod
    def rfind(text: str, search: str, caseSensitive: bool = True) -> int:
        """
        获取子字符串在字符串的最后出现位置

        :param str text:        要被检查的 string
        :param str search:          在 text 中查找这个字符串。
        :param bool caseSensitive:  是否大写小敏感，默认为True
        :return int:    如果是返回最后的索引值，否则返回-1
        """
        pass

    @staticmethod
    def contains(haystack: str, needles: Union[str, Tuple[str], List[str], Set[str]], ignoreCase: bool = False) -> bool:
        """
        判断指定字符串中是否包含另一指定字符串

        :param str haystack:                                            字符串
        :param Union[str, Tuple[str], List[str], Set[str]] needles:     子字符串
        :param bool ignoreCase:         是否区分大小写，默认区分大小写
        :return bool:
        """
        pass

    @staticmethod
    def wrap(value: str, before: str, after: Optional[str] = None) -> str:
        """
        用给定字符串包裹字符串

        :param str value:
        :param str before:
        :param Optional[str] after:
        :return:
        """
        pass

    @staticmethod
    def isJson(value) -> bool:
        """
        确定给定的字符串是否是有效的 JSON

        :param value:
        :return bool:
        """
        pass

    @staticmethod
    def length(value, trim: bool = False) -> int:
        """
        获取字符个数

        :param value:
        :param bool trim:           是否去除前向空格
        :return:
        """
        pass

    @classmethod
    def size(cls, value, encoding: Optional[str] = None) -> int:
        """
        获取字符串的字节个数

        :param value:
        :param encoding:
        :return int:
        """
        pass

    @classmethod
    def limit(cls, text, limit: int = 100, end: str = "...") -> str:
        """
        将字符串以指定长度进行截断

        :param text:            字符串
        :param int limit:       限制最大长度
        :param end:
        :return:
        """
        pass

    @classmethod
    def mask(cls, text: str, index: int, length: Optional[int] = None, character: str = '*') -> str:
        """
        用重复字符掩盖字符串的一部分，并可用于混淆字符串段，例如电子邮件地址和电话号码。

        :param str text:                    字符串
        :param int index:                   起始位置，可以使用负值
        :param Optional[int] length:        掩盖长度，若为负值则使用切片下标
        :param str character:               掩盖字符
        :return:
        """
        pass

    @staticmethod
    def match(pattern: Union[str, re.Pattern], subject: str, flags: int = 0) -> str:
        """
        返回字符串中和指定正则表达式匹配的部分

        :param Union[str, re.Pattern] pattern:          匹配的正则表达式
        :param str subject:                             要匹配的字符串
        :param int flags:                               标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。
        :return:
        """
        pass

    @staticmethod
    def matchAll(pattern: Union[str, re.Pattern], subject: str, flags: int = 0) -> List[str]:
        """
        返回包含了字符串中与指定正则表达式匹配部分的集合

        :param Union[str, re.Pattern] pattern:          匹配的正则表达式
        :param str subject:                             要匹配的字符串
        :param int flags:                               标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。
        :return List[str]:
        """
        pass

    @staticmethod
    def isMatch(pattern: Union[str, re.Pattern, List[str], Tuple[str], List[re.Pattern], Tuple[re.Pattern]], subject: str, flags: int = 0) -> bool:
        """
        用于判断给定的字符串是否与正则表达式匹配

        :param Union[str, re.Pattern, List[str], Tuple[str], List[re.Pattern], Tuple[re.Pattern]] pattern:          匹配的正则表达式
        :param str subject:                             要匹配的字符串
        :param int flags:                               标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。
        :return:
        """
        pass

    @staticmethod
    def padBoth(value: str, length: int, pad: str = ' ') -> str:
        """
        在指定字符串的两侧填充上另一字符串

        :param str value:
        :param int length:
        :param str pad:
        :return:
        """
        pass

    @staticmethod
    def padLeft(value: str, length: int, pad: str = ' ') -> str:
        """
        在指定字符串的左侧填充上另一字符串

        :param str value:
        :param int length:
        :param str pad:
        :return:
        """
        pass

    @staticmethod
    def padRight(value: str, length: int, pad: str = ' ') -> str:
        """
        在指定字符串的右侧填充上另一字符串

        :param str value:
        :param int length:
        :param str pad:
        :return:
        """
        pass

    @staticmethod
    def plural(word: str) -> str:
        """
        将单数形式的字符串转换为复数形式

        :param str word:        单词
        :return:
        """
        pass

    @staticmethod
    def singular(word: str) -> str:
        """
        将字符串转换为其单数形式
        :param word:
        :return str:
        """
        pass

    @classmethod
    def replace(cls, subject: str, search: Union[str, Tuple[str], List[str], Set[str]], replace: str, count: int = 0, caseSensitive: bool = True) -> str:
        """
        用于替换字符串中的给定字符串

        :param str subject:                 要搜索替换的目标字符串
        :param Union[str, Tuple[str], List[str], Set[str]] search:                  要查找的值或数组
        :param str replace:                 替换 `search` 的值
        :param int count:                   替换的最大次数，默认是0（无限制）
        :param bool caseSensitive:          是否大小写敏感
        :return:
        """
        pass

    @classmethod
    def replaceIgnoreCase(cls, subject: str, search: str, replace: str, count: int = 0) -> str:
        """
        用于替换字符串中的给定字符串（不区分大小写）

        :param str subject:                 要搜索替换的目标字符串
        :param str search:                  要查找的值
        :param str replace:                 替换 `search` 的值
        :param int count:         替换的最大次数，默认是0（无限制）
        :return:
        """
        pass

    @staticmethod
    def replaceArray(subject: str, search: str, replace: Union[List[str], Tuple[str]]) -> str:
        """
        使用数组有序的替换字符串中的特定字符

        :param str subject:
        :param str search:
        :param Union[List[str], Tuple[str]] replace:
        :return str:
        """
        pass

    @classmethod
    def replaceFirst(cls, subject: str, search: str, replace: str) -> str:
        """
        替换字符串中给定值的第一个匹配项

        :param str subject:
        :param str search:
        :param str replace:
        :return str:
        """
        pass

    @classmethod
    def replaceLast(cls, subject: str, search: str, replace: str) -> str:
        """
        替换字符串中最后一次出现的给定值

        :param str subject:
        :param str search:
        :param str replace:
        :return str:
        """
        pass

    @classmethod
    def replaceStart(cls, subject: str, search: str, replace: str) -> str:
        """
        替换字符串开头第一个出现的给定值

        :param str subject:
        :param str search:
        :param str replace:
        :return:
        """
        pass

    @classmethod
    def replaceEnd(cls, subject: str, search: str, replace: str) -> str:
        """
        如果给定值出现在字符串末尾，则替换最后出现的值

        :param str subject:
        :param str search:
        :param str replace:
        :return:
        """
        pass

    @staticmethod
    def replaceMatches(subject, pattern: Union[str, re.Pattern], replace: Union[str, Callable], count: int = 0, flags: int = 0):
        """
        用给定的替换字符串替换与模式匹配的字符串的所有部分

        :param str subject:                             要被查找替换的原始字符串
        :param Union[str, re.Pattern] pattern:          要搜索的模式，可以是字符串
        :param Union[str, Callable] replace:            替换的字符串，也可为一个函数
        :param int count:                               可选，对于每个模式用于每个 subject 字符串的最大可替换次数。 默认是0（无限制）
        :param int flags:                               标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等
        :return:
        """
        pass

    @staticmethod
    def substrReplace(subject: str, replace: str, offset: int = 0, length: Optional[int] = None) -> str:
        """
        替换字符串一部分中的文本

        :param str subject:         被检查的字符串
        :param str replace:         要替换或插入的字符串
        :param int offset:          在字符串中何处开始搜索
                                    正数 - 在字符串中的指定位置开始替换
                                    负数 - 在从字符串结尾的指定位置开始替换
                                    0 - 在字符串中的第一个字符处开始替换
        :param Optional[int] length:    要替换多少个字符。默认是与字符串长度相同
                                        正数 - 被替换的字符串长度
                                        负数 - 表示待替换的子字符串结尾处距离 subject 末端的字符个数。
                                        0 - 插入而非替换
        :return str:
        """
        pass

    @staticmethod
    def swap(maps: Dict[str, str], subject: str) -> str:
        """
        替换给定字符串中的多个值

        :param maps:
        :param subject:
        :return:
        """
        pass

    @staticmethod
    def remove(search: Union[str, Tuple[str], List[str], Set[str]], subject: str, caseSensitive: bool = True) -> str:
        """
        用于从字符串中删除给定的值或值数组

        :param Union[str, Tuple[str], List[str], Set[str]] search:      执行替换的数组或者字符串
        :param str subject:     执行替换的数组或者字符串
        :param bool caseSensitive:       是否大小写敏感，默认为区分大小写
        :return:
        """
        pass

    @staticmethod
    def reverse(value: str) -> str:
        """
        反转给定的字符串

        :param str value:     字符串
        :return str:
        """
        pass

    @classmethod
    def startsWith(cls, haystack: str, needles: Union[str, List[str], Tuple[str], Set[str]], caseSensitive: bool = True) -> bool:
        """
        确定给定字符串是否以给定值开头

        :param str haystack:        字符串
        :param Union[str, List[str], Tuple[str], Set[str]] needles:         前缀字符串或集合
        :param bool caseSensitive:  是否大写小敏感，默认为True
        :return bool:       匹配前缀或前缀集合中的其中一个时，返回True
        """
        pass

    @classmethod
    def endsWith(cls, haystack: str, needles: Union[str, List[str], Tuple[str], Set[str]], caseSensitive: bool = True) -> bool:
        """
        用于判断指定字符串是否以另一指定字符串结尾

        :param str haystack:
        :param Union[str, List[str], Tuple[str], Set[str]] needles:         结尾字符串或集合
        :param bool caseSensitive:  是否大写小敏感，默认为True
        :return bool:       匹配结尾或结尾集合中的其中一个时，返回True
        """
        pass

    @staticmethod
    def start(value: str, prefix: str) -> str:
        """
        将给定的值添加到字符串的开始位置

        :param str value:               字符串
        :param str prefix:              指定字符前缀
        :return:
        """
        pass

    @staticmethod
    def finish(value: str, cap: str) -> str:
        """
        将指定的字符串修改为以指定的值结尾的形式

        :param value:       字符串
        :param cap:         指定结尾字符
        :return:
        """
        pass

    @staticmethod
    def lower(value) -> str:
        """
        用于将字符串转换为小写

        :param str value:       字符串
        :return:
        """
        pass

    @staticmethod
    def upper(value) -> str:
        """
        将给定字符串转换为大写

        :param str value:       字符串
        :return:
        """
        pass

    @staticmethod
    def ucsplit(text: str) -> List[str]:
        """
        将给定的字符串按大写字符拆分为数组

        :param text:
        :return:
        """
        pass

    @classmethod
    def headline(cls, text: str) -> str:
        """
        将由大小写、连字符或下划线分隔的字符串转换为空格分隔的字符串，每个单词的首字母大写

        :param str text:
        :return:
        """
        pass

    @staticmethod
    def title(value: str) -> str:
        """
        将给定的字符串转换为 `Title Case`

        :param value:
        :return:
        """
        pass

    @classmethod
    def slug(cls, title: str, sep: str = '-', language: Optional[str] = 'en', dictionary: Optional[Dict[str, str]] = None) -> str:
        """
        TODO：从给定字符串生成 URL 友好的 `“slug”`

        :param str title:
        :param str sep:
        :param Optional[str] language:
        :param Optional[Dict[str, str]] dictionary:
        :return:
        """
        pass

    @classmethod
    def camel(cls, text: str) -> str:
        """
        将指定字符串转换为`camelCase 驼峰式` 表示方法

        :param text:
        :return:
        """
        pass

    @classmethod
    def snake(cls, text: str, sep: str = '_') -> str:
        """
        法将给定字符串转换为 `snake_case`

        :param str text:
        :param str sep:     分隔连接符
        :return:
        """
        pass

    @classmethod
    def studly(cls, text: str) -> str:
        """
        将给定字符串转换为 `StudlyCase`

        :param text:
        :return:
        """
        pass

    @classmethod
    def kebab(cls, text: str) -> str:
        """
        将字符串转换为烤串式（ `kebab-case` ）表示方法

        :param str text:
        :return:
        """
        pass

    @staticmethod
    def squish(text: str) -> str:
        """
        删除字符串中所有无关紧要的空白，包括字符串之间的空白

        :param text:        字符串
        :return str:
        """
        pass

    @staticmethod
    def ucfirst(text: str) -> str:
        """
        返回第一个字符大写的给定字符串

        :param text:
        :return:
        """
        pass

    @staticmethod
    def lcfirst(text: str) -> str:
        """
        返回给定的字符串的第一个字符为小写字母

        :param text:
        :return:
        """
        pass

    @staticmethod
    def substrCount(haystack: str, needle: str, offset: int = 0, length: Optional[int] = None) -> int:
        """
         返回给定字符串中给定值的出现次数

        :param str haystack:        被检查的字符串
        :param str needle:          要搜索的字符串
        :param int offset:          在字符串中何处开始搜索
        :param Optional[int] length:        搜索的长度
        :return:
        """
        pass

    @classmethod
    def password(cls, length: int = 32, letters: bool = True, numbers: bool = True, symbols: bool = True, spaces: bool = False) -> str:
        """
        生成给定长度的安全随机密码

        :param int length:          生成密码长度，默认32
        :param bool letters:        是否必须包含字母
        :param bool numbers:        是否必须包含数字
        :param bool symbols:        是否必须包含符号
        :param bool spaces:         是否必须包含空格
        :return:
        """
        pass

    @staticmethod
    def position(haystack: str, needle: str, caseSensitive: bool = True) -> int:
        """
         查找字符串在另一字符串中第一次出现的位置

        :param str haystack:        被搜索的字符串
        :param str needle:          要查找的字符串
        :param bool caseSensitive:  是否大写小敏感，默认为True
        :return int:        返回字符串在另一字符串中第一次出现的位置，如果没有找到字符串则返回 -1
        """
        pass

    @staticmethod
    def positionLast(haystack: str, needle: str, caseSensitive: bool = True) -> int:
        """
         查找字符串在另一字符串中最后一次出现的位置

        :param str haystack:        被搜索的字符串
        :param str needle:          要查找的字符串
        :param bool caseSensitive:  是否大写小敏感，默认为True
        :return int:        查找字符串在另一字符串中最后一次出现的位置，如果没有找到字符串则返回 -1
        """
        pass

    @staticmethod
    def uuid() -> str:
        """
        生成一个 UUID（版本 4）

        :return:
        """
        pass

    @staticmethod
    def orderedUuid() -> str:
        """
        用于生成一个「时间戳优先」的 UUID

        :return:
        """
        pass

    @staticmethod
    def isUuid(value: str, version: int = 4) -> bool:
        """
        确定给定的字符串是否是一个 UUID

        :param str value:       需要检查的字符串
        :param int version:     指定uuid版本，默认4
        :return bool:
        """
        pass

    @staticmethod
    def ulid() -> str:
        """
        生成一个 ULID

        :return:
        """
        pass

    @staticmethod
    def isUlid(value: str) -> bool:
        """
        确定给定的字符串是否一个 ULID

        :param value:
        :return:
        """
        pass

    @classmethod
    def equal(cls, str1: Any, str2: Any, ignore: bool = False) -> bool:
        """
        判断两个字符串对象是否相等

        :param Any str1:        第一个字符串对象
        :param Any str2:        第二个字符串对象
        :param bool ignore:     是否忽略字符串大小写
        :return bool:
        """
        pass

    @classmethod
    def equalIgnore(cls, str1: Any, str2: Any) -> bool:
        """
        判断两个字符串对象是否相等，忽略大小写

        :param Any str1:        第一个字符串对象
        :param Any str2:        第二个字符串对象
        :return bool:
        """
        pass

    @staticmethod
    def trim(value) -> str:
        """
        字符串去空

        :param value:
        :return:
        """
        pass

    @staticmethod
    def trimPrefix(content, prefix) -> str:
        """
        去除前缀
        :param content:
        :param prefix:
        :return:
        """
        pass

    @staticmethod
    def trimSuffix(content, suffix) -> str:
        """
        去除后缀
        :param content:
        :param suffix:
        :return:
        """
        pass

    @staticmethod
    def longestCommonSubString(*args) -> str:
        """
        搜索字符串列表中最长公共子字符串
        :param args:
        :return:
        """
        pass

