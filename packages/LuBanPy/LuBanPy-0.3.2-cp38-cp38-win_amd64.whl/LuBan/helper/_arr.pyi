#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：Yay 
@File       ：_arr.py
@Author     ：Alex
@Date       ：2023/4/22 18:51 
@Function   ：Arr组件 - 用于列表、字典、集合等工具套件
"""
from typing import Any, Union, List, Set, Tuple, Optional


class Arr:

    KEEP = 'keep'


    @classmethod
    def intersect(cls, arr1: Union[list, tuple, set], arr2: Union[list, tuple, set], ignore: bool = False) -> Union[list, tuple, set, None]:
        """
        交集，返回属于arr1且属于arr2的元素。
        **定义：**
        设A、B两个集合，由所有属于集合A且属于集合B的元素所组成的集合，叫做集合A与集合B的交集。
        在Python中，进行交集运算时使用“&”符号。

        :param Union[list, tuple, set] arr1:        集合对象1
        :param Union[list, tuple, set] arr2:        集合对象2
        :param ignore ignore:                       字符串元素是否忽略大小写
        :return Union[list, tuple, set]:            新的Union[list, tuple, set]对象
        :raises:
            - TypeError                             传入类型必须为Union[list, tuple, set]
        """
        pass

    @classmethod
    def union(cls, arr1: Union[list, tuple, set], arr2: Union[list, tuple, set], ignore: bool = False) -> Union[list, tuple, set, None]:
        """
        返回两个集合的并集，即包含了所有集合的元素，重复的元素只会出现一次。
        **定义：**
        给定两个集合A、B，把他们所有的元素合并在一起组成的集合，叫做集合A与集合B的并集。
        在Python中，进行并集运算时使用“|”符号。

        :param Union[list, tuple, set] arr1:        集合对象1
        :param Union[list, tuple, set] arr2:        集合对象2
        :param ignore ignore:                       元素是否忽略大小写
        :return Union[list, tuple, set]:            新的Union[list, tuple, set]对象
        :raises:
            - TypeError                             传入类型必须为Union[list, tuple, set]
        """
        pass

    @classmethod
    def diff(cls, arr1: Union[list, tuple, set], arr2: Union[list, tuple, set], ignore: bool = False) -> Union[list, tuple, set, None]:
        """
        用于返回集合的差集，即返回的集合元素包含在第一个集合中，但不包含在第二个集合(方法的参数)中。

        **定义：**
        设A，B是两个集合，则所有属于A且不属于B的元素构成的集合，叫做集合A与集合B的差集。
        在Python中，进行差集运算时使用“-”符号。

        :param Union[list, tuple, set] arr1:        集合对象1
        :param Union[list, tuple, set] arr2:        集合对象2
        :param ignore ignore:                       元素是否忽略大小写
        :return Union[list, tuple, set]:            新的Union[list, tuple, set]对象
        :raises:
            - TypeError                             传入类型必须为Union[list, tuple, set]
        """
        pass

    @classmethod
    def setdiff(cls, arr1: Union[list, tuple, set], arr2: Union[list, tuple, set], ignore: bool = False) -> Union[list, tuple, set, None]:
        """
        法返回两个集合中不重复的元素集合，即会移除两个集合中都存在的元素。

        **定义：**
        对称差集也称为对称差分或者补集，设A，B是两个集合，所有不相同的集合，叫做集合A与集合B的对称差集（对称差分或者补集）。
        在Python中，进行对称差集运算时使用“^”符号。

        :param Union[list, tuple, set] arr1:        集合对象1
        :param Union[list, tuple, set] arr2:        集合对象2
        :param ignore ignore:                       元素是否忽略大小写
        :return Union[list, tuple, set]:            新的Union[list, tuple, set]对象
        :raises:
            - TypeError                             传入类型必须为Union[list, tuple, set]
        """
        pass

    @classmethod
    def isdisjoint(cls, arr1: Union[list, tuple, set], arr2: Union[list, tuple, set], ignore: bool = False) -> bool:
        """
        用于判断两个集合是否包含相同的元素，如果没有返回 True，否则返回 False。

        :param Union[list, tuple, set] arr1:        集合对象1
        :param Union[list, tuple, set] arr2:        集合对象2
        :param ignore ignore:                       元素是否忽略大小写
        :return Union[list, tuple, set]:            新的Union[list, tuple, set]对象
        :return bool:
        """
        pass

    @classmethod
    def issubset(cls, arr1: Union[list, tuple, set], arr2: Union[list, tuple, set], ignore: bool = False) -> bool:
        """
        用于判断集合的所有元素是否都包含在指定集合中，如果是则返回 True，否则返回 False。
        判断arr1是否arr2的子集。

        :param Union[list, tuple, set] arr1:        集合对象1
        :param Union[list, tuple, set] arr2:        集合对象2
        :param ignore ignore:                       元素是否忽略大小写
        :return Union[list, tuple, set]:            新的Union[list, tuple, set]对象
        :return bool:
        """
        pass

    @classmethod
    def issuperset(cls, arr1: Union[list, tuple, set], arr2: Union[list, tuple, set], ignore: bool = False) -> bool:
        """
        用于判断指定集合的所有元素是否都包含在原始的集合中，如果是则返回 True，否则返回 False。

        :param Union[list, tuple, set] arr1:        集合对象1
        :param Union[list, tuple, set] arr2:        集合对象2
        :param ignore ignore:                       元素是否忽略大小写
        :return Union[list, tuple, set]:            新的Union[list, tuple, set]对象
        :return bool:
        """
        pass

    @classmethod
    def has(cls, arr: Union[list, tuple, set, dict], val: Any, ignore: bool = True) -> bool:
        """
        检查`list`、`tuple`、`set`、`dict`是否包含值，当`dict`存在嵌套时转换为二维数组再检查平铺的取值列表。

        :param Union[list,tuple,set,dict] arr:      需要检查的数组对象
        :param Any val:                             值，可以任何类型
        :param bool ignore:                         当值为`str`类型时，设置是否区分大小写，True忽略大小写，False区分
        :return bool:
        """
        pass

    @classmethod
    def index(cls, arr: Union[list, tuple, set, dict], val: Any, ignore: bool = True) -> Any:
        """
        返回值的索引或键，`list`、`tuple`返回值的位置，`dict`类型返回值对应的键名，`set`类型如果存在则返回值，与原生区别为可以忽略大小写。

        :param Union[list, tuple, set, dict] arr:     需要检查的数组对象
        :param Any val: 值
        :param bool ignore: 当值为`str`类型时，设置是否区分大小写，True忽略大小写，False区分，默认为True
        :return Any: `list`、`tuple`返回值的位置，`dict`类型返回值对应的键名，`set`类型如果存在则返回值
        :raises
            - TypeError：当arr类型不为list、tuple、set、dict时返回错训
            - KeyError: 当val不存在时，抛出`KeyError`异常。
        """
        pass

    @classmethod
    def append(cls, arr: Union[set, list, dict], key: Any = None, val: Any = None, ignore: bool = False, unique: bool = False, force: Union[bool, str] = 'keep'):
        """
        `list`和`set`追加项，当`ignore`设置True检查值大小写忽略，否则到原`list`类中的`append`方法一致。但当`unique`为`True`时，list也可限制唯一值。
        当为`arr`为`dict`类型及`key`不为空时，则在该arr中的key节点位置append值，如节点不存在时将自动创建新的list。

        :param Union[set, list, dict] arr:          arr列表或集合对象，`dict`类型时，更新节点
        :param Any key:                             键，可使用「.」符号表示层级关系，该方法强制忽略大小写
        :param Any val:                             追加的值，当arr为list或set时，val为None时，val从key获取
        :param bool ignore:                         值为`str`类型时，设置是否区分大小写，True忽略大小写，False区分
        :param bool unique:                         针对`list`类型，是否限制唯一值
        :param Union[bool, str] force:              是否强制覆盖节点类型，False不修改，默认值为True，值为keep时尽显保留节点数据
        :return:
        """
        pass

    @classmethod
    def insert(cls, arr: Union[list, set, dict], key: Any = None, val: Any = None, pos: Union[int, None] = None, ignore: bool = False, unique: bool = False, force: Union[bool, str] = 'keep'):
        """
        在`list`的指定位置`pos`插入值，`ignore` 参数设置值是否区分大写小，`unique`参数是否限制值唯一存在。
        当为`arr`为`dict`类型及`key`不为空时，则在该arr中的key节点位置insert值，如节点不存在时将自动创建新的list。

        :param Union[list, set, dict] arr:          arr列表或集合对象，`dict`类型时，更新节点
        :param Any key:                             键，可使用「.」符号表示层级关系
        :param Any val:                             值,当arr为list或set时，val为None时，val从key获取
        :param int pos:                             插入位置
        :param bool ignore:                         值为`str`类型时，设置是否区分大小写，True忽略大小写，False区分
        :param bool unique:                         是否限制唯一值
        :param Union[bool, str] force:              是否强制覆盖节点类型，False不修改，默认值为True，值为keep时尽显保留节点数据
        :return:
        """
        pass

    @classmethod
    def extend(cls, arr: Union[list, set, dict], key: Any = None, other: Any = None, ignore: bool = False, unique: bool = False, force: Union[bool, str] = 'keep'):
        """
        `list`列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）。对于`set`对象则是扩展列表（并集）。
        当为`arr`为`dict`类型及`key`不为空时，则在该arr中的key节点位置extend新的列表，如节点不存在时将自动创建新的list。

        :param Union[list, set, dict] arr:      arr列表或集合对象，`dict`类型时，更新节点
        :param Any key:                         键，可使用「.」符号表示层级关系，该方法强制忽略大小写
        :param Any other:                       需要追加的序列对象, 当arr为list或set时，other为None时，other从key获取
        :param bool ignore:                     值为`str`类型时，设置是否区分大小写，True忽略大小写，False区分
        :param bool unique:                     是否限制唯一值
        :param Union[bool, str] force:          是否强制覆盖节点类型，False不修改，默认值为True，值为keep时尽显保留节点数据
        :return:
        """
        pass

    @classmethod
    def distinct(cls, arr: Union[list, set, dict], key: Any = None, ignore: bool = True):
        """
        列表去重，`ignore`设置为`True`忽略大小写时`dict`和`set`类型才起作用，`dict`根据键名去重。

        :param Union[list, set, dict] arr:      列表对象，dict和set仅在ignore=True时才进行去重处理
        :param Any key:                         键，可使用「.」符号表示层级关系，用于嵌套的dict处理
        :param bool ignore:                     当值为`str`类型时，设置是否区分大小写，True忽略大小写，False区分
        :return:
        """
        pass

    @classmethod
    def flatten(cls, arr: dict, sep: str = '.', prepend: str = '') -> dict:
        """
        将多维`dict`中所有的键平铺到一维数组`dict`中，新数组使用「.」符号表示层级包含关系

        :param dict arr:        仅支持dict对象
        :param str sep:         嵌套分隔符，默认为「.」
        :param str prepend:     递归前缀
        :return dict:           返回扁平的dict
        """
        pass

    @classmethod
    def dot(cls, arr: dict, ignore: bool = True, unique: bool = True, sep: str = '.') -> dict:
        """
        将使用「点表示法」的一维数组扩展为多维dict

        :param dict arr:        dict对象
        :param bool ignore:     键名是否区分大小写
        :param bool unique:     键值是否唯一
        :param str sep:         键名分隔符
        :return dict:           返回多维的dict
        """
        pass

    @classmethod
    def exists(cls, arr: Union[dict, list, tuple, set], key: Any, ignore: bool = True, sep: Optional[str] = '.') -> bool:
        """
        检查`dict`是否存在键，`list`或`tuple`是否存在索引，`set`是否存在值

        :param Union[dict,list,tuple,set] arr:        需要检查的对象
        :param Any key:         键名、索引或值，可以任何类型，对象为`dic`时t支持「.」级联键名
        :param bool ignore:     当key为`str`类型时，设置是否区分大小写，True忽略大小写，False区分
        :param Optional[str] sep:         嵌套分隔符，默认为「.」
        :return bool:
        """
        pass

    @classmethod
    def searchKey(cls, arr: dict, key: Any, ignore: bool = True, sep: Optional[str] = '.') -> Any:
        """
        搜索dict最匹配的键名。键不存在时抛出KeyError异常。

        :param dict arr:        要求dict对象，否则报TypeError
        :param Any key:         搜索的键名，类型为str时支持「.」级联键名
        :param bool ignore:     当key为`str`类型时，设置是否区分大小写，True忽略大小写，False区分
        :param Optional[str] sep:         嵌套分隔符，默认为「.」
        :return Any:
        :raises:
            TypeError:  arr只能是dict类型
            KeyError:   键不存在时
        """
        pass

    @classmethod
    def merge(cls, *objs, ignore: bool = False, unique: bool = True) -> Union[dict, list, tuple, set, None]:
        """
        合并两对象，返回新的对像
        - 支持迭归合并
        - 低维类型提升为高维类型

        :param Any objs:        需要操作的对象列表
        :param bool ignore:     设置是否区分大小写，True忽略大小写，False区分，同时限制键和值
        :param bool unique:     设置值是否限制唯一值
        :return Union[dict, list, tuple, set, None]:      返回新的对像
        """
        pass

    @classmethod
    def chunk(cls, arr: Union[list, tuple, set], size: int, iterate: bool = True):
        """
        列表分块迭代，arr对像为`list`、`tuple`、`set`

        :param Union[list, tuple, set] arr:     列表对象
        :param int size:                        分块大小
        :param bool iterate:                    是否返回迭代对象，默认值True
        :return:
        """
        pass



    @classmethod
    def update(cls, arr: dict, key: Any, other: Any = None, ignore: bool = True, force: bool = True, sep: Optional[str] = '.'):
        """
        将`other`更新到`arr`项，可使用「.」符号表示层级关系

        :param dict arr:    目标dict对象
        :param Any key:     指定更新的节点（节点也是dict类型，当不存在时，自动添加节点），当key为None时，更新对象是arr，可使用「.」符号表示层级关系
        :param Any other:     需要更新的dict
        :param bool ignore: 当值为`str`类型时，设置是否区分大小写，True忽略大小写，False区分
        :param bool force: 是否强制覆盖节点类型，False不修改，默认值为True
        :param Optional[str] sep:         嵌套分隔符，默认为「.」
        :return:
        :raise TypeError 当操作对象类型正常确时抛出异常
        """
        pass

    @classmethod
    def remove(cls, arr: Union[dict, list, set], key: Any = None, val: Any = None, pos: Union[int, List[int], Tuple[int], Set[int]] = -1, ignore: bool = True, limit: int = 1):
        """
        删除`arr`中的项，`dict`类型时根据`key`键删除，list和set类型时根据`val`值删除，当list时还可以指定pos指定删除位置。

        :param Union[dict, list, set] arr:      arr对象
        :param Any key:         键，可使用「.」符号表示层级关系，当arr不为dict时并且val为None时交换为val值
        :param Any val:         值,当arr为list或set时，val为None时，val从key获取
        :param int pos:         按索引位置删除，当操作对象为list和pos>=0时优先于val
        :param bool ignore:     值为`str`类型时，设置是否区分大小写，True忽略大小写，False区分
        :param int limit:       限制最大删除数量，0不限制，默认值1
        :return:
        """
        pass

    @classmethod
    def get(cls, arr: Union[dict, tuple, list, set], key: Any, default: Any = None, ignore: bool = True, sep: Optional[str] = '.') -> Any:
        """
        获取`dict`项，可使用「.」符号表示层级关系

        :param Union[dict, tuple, list] arr:        arr操作对象
        :param Any key:         键，可使用「.」符号表示层级关系
        :param Any default:     设置返回默认值，默认为None
        :param bool ignore:     键为字符串类型时，设置是否区分大小写，True忽略大小写，False区分
        :param Optional[str] sep:         节点分隔符，默认为「.」
        :return Any:            存时时返回节点值，不存在返回默认值
        """
        pass

    @classmethod
    def set(cls, arr: dict, key: Any, val: Any = None, ignore: bool = True, sep: Optional[str] = '.', force: Union[bool, str] = True, unique: bool = True):
        """
        设置`dict`项，可使用「.」符号表示层级关系

        :param dict arr:        dict操作对象
        :param Any key:         键，可使用「.」符号表示层级关系
        :param Any val:         值，设置节点的值
        :param bool ignore:     当值为`str`类型时，设置是否区分大小写，True忽略大小写，False区分
        :param Optional[str] sep:         节点分隔符，默认为「.」
        :param Union[bool, str] force:      是否强制覆盖节点类型，False不修改，默认值为True，值为keep时尽显保留节点数据
        :param bool unique:                 节点合并时是否限制值唯一
        :return:
        """
        pass


