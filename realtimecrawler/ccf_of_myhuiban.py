#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/29 18:39
# @Author  : ZengJunMing
# @File    : testbaidu.py

"""
爬取CCF会议信息
"""
import json
import re

import requests
import time
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

from dao.conferenceDao import saveConferenceSet, updateConferenceSet
from util.mysqlhelper import Mysql
from util.typeconverter import Converter


def writeToFile(fileName, content, encoding='utf-8', pattern='a'):
    with open(fileName, pattern, encoding=encoding)as f:
        f.write(content)

def writeToJson(dictionary, filename, pattern="a"):
    with open(filename, pattern, encoding='utf-8') as f:
        f.write(json.dumps(dictionary, ensure_ascii=False))

session_requests = requests.session()
loginUrl = "https://www.myhuiban.com/login"

data = {
    'LoginForm[email]': '1102360628@qq.com',
    'LoginForm[password]': '10070107',
    'LoginForm[rememberMe]': 1,
    'yt0': '登录'
}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Origin': "https://www.myhuiban.com",
    'Referer': 'https://www.myhuiban.com/login',
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/65.0.3325.181 Safari/537.36"}

result = session_requests.post(loginUrl, data=data, headers=headers).text
base_list = []


for i in range(1, 17):
    url = "https://www.myhuiban.com/conferences?Conference_page=" + str(i) + "&ajax=yw2"
    result = session_requests.get(url, headers=headers).text
    doc = pq(result)
    tr = doc("#yw2 > table:nth-child(2) > tbody:nth-child(2) > tr")
    # print(tr)
    for item in tr:
        td = pq(item)
        tag = td("tr > td:nth-child(1) > span:nth-child(1)").text()
        href_tag = {}
        if tag in "abc" and tag != "":
            href = "https://www.myhuiban.com" + td('a').attr('href')
            href_tag = {'tag': tag,
                        'href': href}
            print(href_tag)
            base_list.append(href_tag)

info = []
href_dict = {}
for it in base_list:
    url = it.get('href')
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
    html = session_requests.get(url, headers=header).text
    soup = BeautifulSoup(html, "lxml")
    try:
        content = soup.find_all("div", attrs={"class": "portlet-content"})[0]
        tag_text = content.find_all("div", attrs={"class": "hidden-phone"})[0].get_text()
        # print(tag_text)
        if "CCF" in tag_text:
            enName = content.find("h5").get_text()
            website = content.find("a").get("href")
            startdate1 = content.find_all("tr")[2].find_all("td")[1].get_text()
            startdate = re.compile(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}").findall(startdate1)
            location = content.find_all("tr")[3].find_all("td")[1].get_text()
            deadline1 = content.find_all("tr")[0].find_all("td")[1].get_text()
            deadline = re.compile(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}").findall(deadline1)
            tag = content.find_all("div", attrs={"class": "hidden-phone"})[0].find("span").get_text()
            if enName != "":
                href_dict["enName"] = enName
            if startdate != "":
                href_dict["startdate"] = startdate
            if deadline != "":
                href_dict["deadline"] = deadline
            if website != "":
                href_dict["website"] = website
            if tag != "":
                href_dict["tag"] = "CCF-" + it.get('tag').upper()
            if location != "":
                href_dict["location"] = location
            print(href_dict)
            info.append(href_dict)
        href_dict = {}
    except:
        continue

# print(info)


length = len(info)
i = 0
fileName = "CCF1.json"

writeToFile(fileName, '[\n')
for value in info:
    writeToJson(value, fileName)
    if i != length - 1:
        writeToFile(fileName, ',\n')
    i += 1
    print(i)
writeToFile(fileName, '\n]')
currentset = set()
presistenceset = set()
b = str(Mysql.queryData("select website from ConferenceInfo"))
for dic in info:

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