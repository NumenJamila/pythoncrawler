#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/4 19:19
# @Author  : ZengJunMing
# @File    : main.py

"""
爬取单个会议
"""
import datetime

import os

from .logmanage import loadLogger
from .conferenceDao import saveConferenceSet
from .conferenceDao import updateConferenceSet
from multiprocessing import Queue

from .fileoperate import clearContent, getFileNames
from .mysqlhelper import Mysql
from .typeconverter import Converter
from .extractkeyword import get_info
from .getconffile import get_conf_online
from . import configsetting as cs

def input():
    get_info(item, itemqueue)
    currentset = set()  # 需要插入的信息对象集合
    presistenceset = set()  # 需要更新的信息对象集合
    b = str(Mysql.queryData("select website from " + cs.db_table))  # 根据网址决定是要插入还是更新
    while not itemqueue.empty():
        #  从队列中取出解析后会议信息字典
        dic = itemqueue.get()
        website = dic.get("website")
        #  将字典转换为Conference 对象
        c = Converter.convert_dict_to_entry(dic)
        if website not in b:
            #  将Conference 对象添加到当前集合里
            currentset.add(c)
        else:
            presistenceset.add(c)
    updateConferenceSet(presistenceset)
    saveConferenceSet(currentset)  # 把新爬取的会议信息保存到Mysql

