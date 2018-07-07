#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/24 22:20
# @Author  : ZengJunMing
# @File    : wikicfp.py
"""
爬取wikicfp网站的会议信息, "machine learning", "artificial intelligence",
            "data mining", "security"
"""
import re

from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from queue import Queue

from dao.conferenceDao import updateConferenceSet, saveConferenceSet
from util.mysqlhelper import Mysql
from util.typeconverter import Converter
from util.urllibhelper import SpiderApi


def get_info(final_list):
    for m in final_list:
        detail_html = SpiderApi.getPageSourceCode(m)
        # soup2 = BeautifulSoup(detail_html, "lxml")
        doc = pq(detail_html)
        try:
            enName = doc('body > div:nth-child(5) > center > table > tr:nth-child(2) > td > h2 > span > span:nth-child(7)').text()
        except Exception as e:
            print(e)
        try:
            website = doc('body > div:nth-child(5) > center > table > tr:nth-child(3) > td > a').text()
        except Exception as e:
            print(e)
        try:
            startdate = doc('body > div:nth-child(5) > center > table > tr:nth-child(5) > td > table > tr > td > table > tr:nth-child(1) > td > table > tr:nth-child(1) > td').text()
            startdate = (re.compile("([a-zA-Z]{3} *[0-9]{1,2}, *[0-9]{4}) *-").findall(startdate))[0]
        except Exception as e:
            print(e)
        try:
            enddate = doc('body > div:nth-child(5) > center > table > tr:nth-child(5) > td > table > tr > td > table > tr:nth-child(1) > td > table > tr:nth-child(1) > td').text()
            enddate = (re.compile("- *([a-zA-Z]{3} *[0-9]{1,2}, *[0-9]{4})").findall(enddate))[0]
        except Exception as e:
            print(e)
        try:
            deadline = doc('body > div:nth-child(5) > center > table > tr:nth-child(5) > td > table > tr > td > table > tr:nth-child(1) > td > table > tr:nth-child(3) > td > span > span:nth-child(3)').text()
        except Exception as e:
            print(e)
        try:
            location = doc('body > div:nth-child(5) > center > table > tr:nth-child(5) > td > table > tr > td > table > tr:nth-child(1) > td > table > tr:nth-child(2) > td').text()
        except Exception as e:
            print(e)
        tag = tag_map.get(item)
        print(enName)
        print(website)
        print(startdate)
        print(enddate)
        print(deadline)
        print(location)
        print(tag)
        info_dict = {}
        if enName != "":
            info_dict["enName"] = enName
        if location != "":
            info_dict["location"] = location
        if startdate != "":
            info_dict["startdate"] = startdate
        if enddate != "":
            info_dict["enddate"] = enddate
        if deadline != "":
            info_dict["deadline"] = deadline
        if website != "":
            info_dict["website"] = website
        if tag != "":
            info_dict["tag"] = tag
        info.put(info_dict)

if __name__ == '__main__':
    url_list = ["computer science", "machine learning", "artificial intelligence",
                "data mining", "security"]
    tag_map = {"computer science": "计算机科学", "artificial intelligence": "人工智能",
               "machine learning": "机器学习", "data mining": "数据挖掘", "security": "网络与信息安全"}
    final_list = set()
    info = Queue()

    for item in url_list:
        for i in range(1, 2):
            url = "http://www.wikicfp.com/cfp/call?conference=" + item + "&page=" + str(i)
            print(url)
            html = SpiderApi.getPageSourceCode(url)
            soup = BeautifulSoup(html, "lxml")
            try:
                item_list = soup.find_all("tr", attrs={"bgcolor": "#e6e6e6"})
            except Exception as e:
                print(e)
            for x in item_list:
                try:
                    href = x.find('a').get('href')
                    # print(href)
                    final_list.add("http://www.wikicfp.com" + href)
                except:
                    pass

        get_info(final_list)
    currentset = set()
    presistenceset = set()
    b = str(Mysql.queryData("select website from ConferenceInfo"))
    while not info.empty():
        #  从队列中取出解析后会议信息字典
        dic = info.get()
        try:
            if dic.get("startdate") != "":
                website = dic.get("website")
                c = Converter.convert_dict_to_entry(dic)

                if website not in b:
                    #  将Conference 对象添加到当前集合里
                    currentset.add(c)
                else:
                    presistenceset.add(c)
        except:
            pass
    # 把新爬取的会议信息保存到Mysql
    saveConferenceSet(currentset)
    updateConferenceSet(presistenceset)