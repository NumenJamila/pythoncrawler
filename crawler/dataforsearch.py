#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/15 17:15
# @Author  : ZengJunMing
# @File    : dataforsearch.py
"""
爬取酒店搜索引擎信息
"""
import json

from crawler.util.mysqlhelper import Mysql
from tools import *
from bs4 import BeautifulSoup

def extract_info(html):
    value = {}
    all_info = []
    soup = BeautifulSoup(html, "lxml")
    div_list = soup.find_all("div", attrs={"class": "h_item mvt_171218"})
    for item in div_list:
        name = item.find_all("div", attrs={"class": "h_info_base"})[0].find_all("span", attrs={"class": "info_cn"})[0].get_text()
        address = item.find_all("span", attrs={"class": "l1"})[0].get('data-hoteladdress')
        website = item.find("a").get('href')
        price = item.find_all("span", attrs={"class": "h_pri_num "})[0].get_text()
        level = item.find_all("i", attrs={"class": "t20 c37e"})[0].get_text()
        try:
            hotel_type = item.find_all("p", attrs={"class": "h_info_b1"})[0].find_all("b")[0].get('title').replace("艺龙用户评定为", "")
        except:
            hotel_type = "暂无评定"
        value["address"] = address
        value["name"] = name
        value["website"] = "http://hotel.elong.com" + website
        value["level"] = float(level)
        value["price"] = price
        value["location"] = location
        value["hotel_type"] = hotel_type
        all_info.append(value)
        value = {}
    return all_info


if __name__ == '__main__':
    location = input("请输入地址：")  # 如：惠州      http://hotel.elong.com/
    a = "http://hotel.elong.com/"
    url = input("请输入该地址的拼音:")  #如：huizhou/
    url = url + a
    response = SpiderApi.getPageSourceCode(url)  # 获得网页源代码
    all_info = extract_info(response)  # 获得该页面的关于酒店的信息点
    fields = ["name", "location", "website", "address", "price", "hotel_type", "level"]
    for item in all_info:
        Mysql.saveObject(item, "info", fields)  # 插入数据库