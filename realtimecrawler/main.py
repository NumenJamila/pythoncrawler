#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/4 19:19
# @Author  : ZengJunMing
# @File    : main.py

"""
爬取单个会议
"""
from datetime import datetime
from multiprocessing import Pool

from bs4 import BeautifulSoup

from tools import *
from util.fileoperate import *
from util.typeconverter import Converter


def get_info(item):
    cfg = readConfig(item)[0]
    website = cfg.get("website_select")

    html = SpiderApi.getPageSourceCode(website)
    soup = BeautifulSoup(html, "lxml")

    cnName = cfg.get("cnname_select")
    cnName_reg = cfg.get("cnname_reg")
    # print("cnName_reg:" + cnName_reg)
    try:
        if cnName == "":
            cnName = cnName_reg
        else:
            cnName = soup.select(cnName)[0].get_text()
            if cnName_reg != "null":
                cnName = re.findall(cnName_reg, cnName)[0]
    except Exception as e:
        print("cnName:" + str(e))
        cnName = ""

    enName = cfg.get("enname_select")
    enName_reg = cfg.get("enname_reg")
    # print("enName_reg:" + enName_reg)
    try:
        if enName == "":
            enName = enName_reg
        else:
            enName = soup.select(enName)[0].get_text()
            if enName_reg != "null":
                enName = re.findall(enName_reg, enName)[0]
    except Exception as e:
        print("enName:" + str(e))
        enName = ""

    introduce = cfg.get("introduce_select")
    introduce_reg = cfg.get("introduce_reg")
    # print("introduce_reg：" + introduce_reg)
    try:
        if introduce == "":
            introduce = introduce_reg
        else:
            introduce = soup.select(introduce)[0].get_text()
            if introduce_reg != "null":
                introduce = re.findall(introduce_reg, introduce)[0]
    except Exception as e:
        print("introduce:" + str(e))
        introduce = ""

    location = cfg.get("location_select")
    location_reg = cfg.get("location_reg")
    # print("location_reg:" + location_reg)
    try:
        if location == "":
            location = location_reg
        else:
            location = soup.select(location)[0].get_text()
            if location_reg != "null":
                location = re.findall(location_reg, location)[0]
    except Exception as e:
        print("location:" + str(e))
        location = ""

    sponsor = cfg.get("sponsor_select")
    sponsor_reg = cfg.get("sponsor_reg")
    # print("sponsor_reg:" + sponsor_reg)
    try:
        if sponsor == "":
            sponsor = sponsor_reg
        else:
            sponsor = soup.select(sponsor)[0].get_text()
            if sponsor_reg != "null":
                sponsor = re.findall(sponsor_reg, sponsor)[0]
    except Exception as e:
        print("sponsor:" + str(e))
        sponsor = ""

    startdate = cfg.get("startdate_select")
    startdate_reg = cfg.get("startdate_reg")
    # print("startdate_reg:" + startdate_reg)
    try:
        if startdate == "":
            startdate = startdate_reg
        else:
            startdate = soup.select(startdate)[0].get_text()
            print(startdate)
            if startdate_reg != "null":
                try:
                    startdate = re.findall(eval(startdate_reg), startdate)[0]
                except:
                    startdate = re.findall(startdate_reg, startdate)[0]
                print(startdate)
    except Exception as e:
        print("startdate:" + str(e))

    deadline = cfg.get("deadline_select")
    deadline_reg = cfg.get("deadline_reg")
    # print("deadline_reg:" + deadline_reg)
    try:
        if deadline == "":
            deadline = deadline_reg
        else:
            deadline = soup.select(deadline)[0].get_text()
            print(deadline)
            if deadline_reg != "null":
                try:
                    deadline = re.findall(eval(deadline_reg), deadline)[0]
                except:
                    deadline = re.findall(deadline_reg, deadline)[0]
                print(deadline)
    except Exception as e:
        print("deadline:" + str(e))

    tag = cfg.get("tag_select")
    tag_reg = cfg.get("tag_reg")
    # print("tag_reg:" + tag_reg)
    try:
        if tag == "":
            tag = tag_reg
        else:
            tag = soup.select(tag)[0].get_text()
            if tag_reg != "null":
                tag = re.findall(eval(tag_reg), tag)[0]
    except Exception as e:
        print("tag:" + str(e))

    image = cfg.get("image_select")
    image_reg = cfg.get("image_reg")
    # print("image_reg:" + image_reg)
    try:
        if image == "":
            image = image_reg
        else:
            image = soup.select(image)[0].get("src")
            print(image)
            if website not in image:
                image = website + image
            if image_reg != "null":
                image = re.findall(eval(image_reg), tag)[0]
    except Exception as e:
        print("image:" + str(e))
        image = ""

    # 将如2018-5-22日期的格式转换成真实时间日期
    try:
        startdate, enddate = DateFormatHelper.convertStandardDateFormat(startdate)
        tmp = startdate.split("-")
        if len(tmp) == 3:
            startdate = datetime(int(tmp[0]), int(tmp[1]), int(tmp[2]))
    except Exception as e:
        print(e)

    try:
        tmp1 = enddate.split("-")
        if len(tmp) == 3:
            enddate = datetime(int(tmp1[0]), int(tmp1[1]), int(tmp1[2]))
    except Exception as e:
        print(e)

    try:
        deadline = DateFormatHelper.convertStandardDateFormat(deadline)[0]
        tmp2 = deadline.split("-")
        if len(tmp2) == 3:
            deadline = datetime(int(tmp2[0]), int(tmp2[1]), int(tmp2[2]))
    except Exception as e:
        print(e)

    # 获得的信息点以字典形式存储
    info_dict = {}
    info_dict["cnName"] = cnName
    info_dict["enName"] = enName
    info_dict["location"] = location
    info_dict["introduce"] = introduce
    info_dict["sponsor"] = sponsor
    if startdate != "":
        info_dict["startdate"] = startdate
    if enddate != "":
        info_dict["enddate"] = enddate
    if deadline != "":
        info_dict["deadline"] = deadline
    info_dict["website"] = website
    info_dict["tag"] = tag
    info_dict["image"] = image
    print(info_dict)
    # showkeydic(info_dict)
    return info_dict

def showkeydic(keydic: dict, resultQueue=None):
    if len(keydic) > 2:
        if resultQueue:
            resultQueue.put(keydic)
    for k, v in keydic.items():
        print("{k} : {v}".format(k=k, v=v))

def put(dic: dict):
    global itemqueue
    if len(dic) > 2:
        itemqueue.put(dic)

if __name__ == "__main__":
    configFileNames = getFileNames('file/configreg/')
    # configFileNames = ["file/configreg/website5.conf"]
    itemqueue = Queue()

    # 创建进程池
    processpool = Pool(processes=2)

    for item in configFileNames:
        print(item)
        processpool.apply_async(get_info, (item,), callback=put,)

    processpool.close()
    processpool.join()

    fields = [
        "cnName",
        "enName",
        "website",
        "tag",
        "image",
        "location",
        "sponsor",
        "startdate",
        "enddate",
        "deadline",
        "introduce",
    ]
    table_str = "ConferenceInfo"
    # conferences = readDictionary(fileName)
    # date1 = dt.date.today()
    b = str(Mysql.queryData("select website from ConferenceInfo"))
    conferences = set()
    while not itemqueue.empty():
        dic = itemqueue.get()

        #  将字典转换为Conference 对象
        c = Converter.convert_dict_to_entry(dic)
        conferences.add(c)
    if len(conferences)==0:
        print("weikong")
    # for element in conferences:
    #     website = element.get("website")
    #     print(website)
    #     if website not in b:
    #         Mysql.saveObject(element, table_str, fields)
    #     else:
    #         Mysql.mysql_update(element, table_str, fields, website)
    for element in conferences:
        Mysql.saveObject(element, table_str, fields)
