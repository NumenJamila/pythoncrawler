#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/13 10:25
# @Author  : ZengJunMing
# @File    : image.py
from util.mysqlhelper import Mysql
import datetime
from util.urllibhelper import SpiderApi

date1 = datetime.date.today()
date2 = date1 + datetime.timedelta(days=6)
print(date2)
# a = Mysql.queryData("select * from ConferenceInfo where startdate=?", params=date2)
a = Mysql.queryData("select ID, image from ConferenceInfo")
for item in a:
    filename = "file/image/"+str(item[0]) + ".png"
    print(item[1])
    try:
        content = SpiderApi.getBinContent(item[1]).content
        with open(filename, "wb") as f:
            f.write(content)
    except Exception as e:
        print(e)