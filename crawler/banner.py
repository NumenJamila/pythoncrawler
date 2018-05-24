#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/13 10:25
# @Author  : ZengJunMing
# @File    : banner.py
from crawler.util.mysqlhelper import Mysql
import datetime
# from main import *
from tools import SpiderApi

date1 = datetime.date.today()
date2 = date1 + datetime.timedelta(days=3)
print(date2)
# a = Mysql.queryData("select * from ConferenceInfo", params=(date1, date2))
a = Mysql.queryData("select ID, banner from ConferenceInfo")
for item in a:
    filename = "file/banner/"+str(item[0]) + ".png"
    print(item[1])
    try:
        content = SpiderApi.getBinContent(item[1]).content
        with open(filename, "wb") as f:
            f.write(content)
    except Exception as e:
        print(e)