#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114,C0103
import re
from typing import Union

import easyprocess
from funnylog import logger

from youqu_dogtail.install_depends import install_depends

install_depends()

from youqu_dogtail.dogtail.tree import SearchError
from youqu_dogtail.dogtail.tree import root
from youqu_dogtail.dogtail.tree import predicate
from youqu_dogtail.dogtail.tree import config
from youqu_dogtail.dogtail.tree import Node

config.childrenLimit = 10000
# config.logDebugToStdOut = False
config.logDebugToFile = False
config.searchCutoffCount = 2


class ElementNotFound(BaseException):
    """未找到元素"""

    def __init__(self, name):
        """
        未找到元素
        :param name: 命令
        """
        err = f"====未找到“{name}”元素！===="
        logger.error(err)
        BaseException.__init__(self, err)


class ApplicationStartError(BaseException):
    """
    应用程序未启动
    """

    def __init__(self, result):
        """
        应用程序未启动
        :param result: 结果
        """
        err = f"应用程序未启动,{result}"
        logger.error(err)
        BaseException.__init__(self, err)


class DogtailUtils():

    __author__ = "mikigo<huangmingqiang@uniontech.com>"

    def __init__(
            self,
            name=None,
            description=None,
            number=-1,
            check_start=True,
            key: dict = None
    ):
        config.logDebugToStdOut = False
        self.name = name
        self.description = description
        try:
            if name:
                self.obj = root.application(self.name, self.description)
            else:
                self.obj = root
            if number > 0:
                self.obj = self.obj.findChildren(predicate.GenericPredicate(**key))[number]

        except SearchError:
            if check_start:
                search_app = easyprocess.EasyProcess(f"ps -ef | grep {self.name}").call().stdout
                logger.error(search_app)
                raise ApplicationStartError(self.name) from SearchError

    def ele(self, *args, **kwargs) -> Node:
        """
         获取app元素的对象
        :return: 元素的对象
        """
        try:
            element = self.obj.child(*args, **kwargs, retry=False)
            logger.debug(f"{args, kwargs} 获取元素对象 <{element}>")
            return element
        except SearchError:
            raise ElementNotFound(*args, **kwargs) from SearchError

    def right_upper_corner_position(self, element) -> tuple:
        """
         获取元素右上角的坐标
        :param element: 元素名称
        :return: 元素右上角坐标
        """
        _x = self.ele(element).position[0] + self.ele(element).size[0]
        _y = self.ele(element).position[1]
        logger.debug(f"获取元素 {element}, 右上角坐标 ({_x, _y})")
        return int(_x), int(_y)

    def element_center(self, element) -> tuple:
        """
         获取元素的中心位置
        :param element:
        :return: 元素中心坐标
        """
        _x, _y, _w, _h = self.ele(element).extents
        _x = _x + _w / 2
        _y = _y + _h / 2
        logger.debug(f"获取元素中心坐标 ({_x, _y})")
        return _x, _y

    @staticmethod
    def __evalx(expr, element, recursive):
        """evalx"""
        node = re.match(".*?[^\\\\]/", expr)
        if node:
            name = node.group().replace("\\/", "/")[:-1]
        else:
            return False
        if name == "*":
            element = element.children
        else:
            element = element.findChildren(predicate.GenericPredicate(name), recursive=recursive)
        return node, element

    def __trace(self, element, result, expr):
        if expr.startswith("//"):
            name = expr[2:]
            node, element = self.__evalx(name, element, recursive=True)
        elif expr.startswith("/"):
            name = expr[1:]
            node, element = self.__evalx(name, element, recursive=False)
        else:
            return False
        try:
            next_node = name[node.end() - 1:]
            if next_node != "/":
                for i in element:
                    self.__trace(i, result, next_node)
            else:
                result += element
        except SearchError:
            raise ElementNotFound(expr) from SearchError
        return result

    def eles_expr(self, expr) -> Union[list, bool]:
        """
         通过层级获取元素
        :param expr: 元素定位 $/xx.xxx//xxx,  $根节点  /当前子节点， //递归查找子节点
        :return: 元素对象
        """
        logger.debug(f"查找元素 expr={expr}")
        if expr == "$":
            return self.obj if isinstance(self.obj, list) else [self.obj]
        if not expr.startswith("$"):
            return False
        if not expr.endswith("/") or expr.endswith(r"\/"):
            expr = expr + "/"
        result = self.__trace(self.obj, [], expr[1:])
        logger.debug(f"元素 {result}")
        return result

    def ele_expr(self, expr, index=0) -> Node:
        """
         查找界面元素
        :param expr: 匹配格式 元素定位 $/xxx//xxx,  $根节点  /当前子节点， //递归查找子节点
        :param index: 匹配结果索引
        :return: 元素对象
        """
        elements = self.eles_expr(expr)
        if not elements:
            raise ElementNotFound(expr)
        try:
            return elements[index]
        except IndexError:
            raise ElementNotFound(f"{expr}, index:{index}") from IndexError

    def click_ele_expr(self, expr, index=0):
        self.ele_expr(expr, index).click()

    def right_click_ele_expr(self, expr, index=0):
        self.ele_expr(expr, index).click(3)


if __name__ == '__main__':
    dog = DogtailUtils().ele("Btn_文件管理器").click()
