#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/14 16:21
# @Author  : ZengJunMing
# @File    : extractkeyword.py
import configsetting as cs
from .fileoperate import readConfig
from .urllibhelper import SpiderApi
from pyquery import PyQuery as pq
import re


def get_info(item, itemqueue):
    per_info_key = cs.fields
    per_info_value = []
    cfg = readConfig(item)[0]
    req_rul = cfg.get("req_url")
    # print(req_rul)
    html = SpiderApi.getPageSourceCode(req_rul)
    doc = pq(html)
    for it in range(0, len(per_info_key)):
        try:
            per_info_value.append((doc(cfg.get(str(per_info_key[it]) + "_select")).text()))
            # print(per_info_value[it])
        except:
            per_info_value.append("")
        if cfg.get(per_info_key[it] + "_reg") != "null" and cfg.get(per_info_key[it] + "_reg"):
            try:
                per_info_value[it] = re.findall(cfg.get(per_info_key[it] + "_reg"), per_info_value[it])[0]
            except Exception as e:
                print(e)
        if cfg.get(per_info_key[it] + "_select") == "pass":
            per_info_value[it] = cfg.get(per_info_key[it] + "_reg")
    # 获得的信息点以字典形式存储
    info_dict = {}
    for i in range(0, len(per_info_key)):
        if per_info_value[i] != "":
            info_dict[per_info_key[i]] = per_info_value[i]
            print(per_info_key[i] + " : " + per_info_value[i])
    itemqueue.put(info_dict)