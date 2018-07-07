#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/4 19:19
# @Author  : ZengJunMing
# @File    : main.py

"""
爬取单个会议
"""
from dao.conferenceDao import saveConferenceSet
from dao.conferenceDao import updateConferenceSet
from multiprocessing import Pool
from multiprocessing import Queue
import re
from pyquery import PyQuery as pq

from util.mysqlhelper import Mysql
from util.urllibhelper import SpiderApi

from util.fileoperate import *
from util.typeconverter import Converter
import get_conf


def get_info(item):
    per_info_key = ['website', 'cnName', 'enName', 'introduce',
                    'location', 'sponsor', 'startdate', 'enddate',
                    'deadline', 'image', 'tag']
    per_info_value = []
    cfg = readConfig(item)[0]
    req_rul = cfg.get("req_url")
    print(req_rul)
    html = SpiderApi.getPageSourceCode(req_rul)
    doc = pq(html)
    for it in range(0, len(per_info_key)):
        try:
            per_info_value.append((doc(cfg.get(str(per_info_key[it]) + "_select")).text()))
            print(per_info_value[it])
        except:
            per_info_value.append("")
        if cfg.get(per_info_key[it] + "_reg") != "null" and cfg.get(per_info_key[it] + "_reg"):
            try:
                per_info_value[it] = re.findall(eval(cfg.get(per_info_key[it] + "_reg")), per_info_value[it])[0]
            except IndexError:
                per_info_value[it] = re.findall(cfg.get(per_info_key[it] + "_reg"), per_info_value[it])[0]
            except Exception as e:
                print(e)

        if cfg.get(per_info_key[it] + "_reg") == "pass":
            per_info_value[it] = cfg.get(per_info_key[it] + "_reg")
    # 获得的信息点以字典形式存储
    info_dict = {}
    for i in range(0, len(per_info_key)):
        if per_info_value[i] != "":
            info_dict[per_info_key[i]] = per_info_value[i]
            print(per_info_key[i] + " : " + per_info_value[i])
    global itemqueue
    itemqueue.put(info_dict)


if __name__ == "__main__":
    get_conf.get_conf_online()
    configFileNames = getFileNames('file/configreg/')
    # configFileNames = ["file/configreg/website1.conf"]
    itemqueue = Queue()
    # 创建进程池

    for item in configFileNames:
        print(item)
        get_info(item)

    currentset = set()
    b = str(Mysql.queryData("select website from check_conferenceinfo"))
    presistenceset = set()  # 需要更新的conference信息对象集合
    while not itemqueue.empty():
        #  从队列中取出解析后会议信息字典
        dic = itemqueue.get()
        website = dic.get("website")
        #  将字典转换为Conference 对象
        c = Converter.convert_dict_to_entry(dic)
        # entry = Converter.convert_dict_to_entry(record)

        if website not in b:
            #  将Conference 对象添加到当前集合里
            currentset.add(c)
        else:
            # Mysql.mysql_update(element, table_str, fields, website)
            presistenceset.add(c)
        # 把新爬取的会议信息保存到Mysql
    updateConferenceSet(presistenceset)
    saveConferenceSet(currentset)

