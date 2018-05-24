#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/4 19:19
# @Author  : ZengJunMing
# @File    : simpletest.py

"""
爬取单个会议
"""
from datetime import datetime
import datetime as dt

from bs4 import BeautifulSoup

from crawler.util.mysqlhelper import Mysql
from tools import *
from crawler.util.fileoperate import *


def get_info(item):
    cfg = readConfig(item)[0]
    cnName = cfg.get("cnname_select")
    enName = cfg.get("enname_select")
    tag = cfg.get("tag_select")
    description = cfg.get("description_select")
    location = cfg.get("location_select")
    sponsor = cfg.get("sponsor_select")
    startdate = cfg.get("startdate_select")
    deadline = cfg.get("deadline_select")
    banner = cfg.get("banner_select")
    website = cfg.get("website_select")


    cnName_reg = cfg.get("cnname_reg")
    print(cnName_reg)

    enName_reg = cfg.get("enname_reg")
    print(enName_reg)

    description_reg = cfg.get("description_reg")
    print(description_reg)

    location_reg = cfg.get("location_reg")
    print(location_reg)

    sponsor_reg = cfg.get("sponsor_reg")
    print(sponsor_reg)

    startdate_reg = cfg.get("startdate_reg")
    print(startdate_reg)

    deadline_reg = cfg.get("deadline_reg")
    print(deadline_reg)

    tag_reg = cfg.get("tag_reg")
    print(tag_reg)

    banner_reg = cfg.get("banner_reg")
    print(banner_reg)

    html = SpiderApi.getPageSourceCode(website)
    soup = BeautifulSoup(html, "lxml")

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
    try:
        if description == "":
            description = description_reg
        else:
            description = soup.select(description)[0].get_text()
            if description_reg != "null":
                description = re.findall(description_reg, description)[0]
    except Exception as e:
        print("description:" + str(e))
        description = ""

    try:
        if location == "":
            location = location_reg
        else:
            location = soup.select(location)[0].get_text()
            if location_reg != "null":
                location = re.findall(location_reg, tag)[0]
    except Exception as e:
        print("location:" + str(e))
        location = ""
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
    try:
        if startdate == "":
            startdate = startdate_reg
        else:
            startdate = soup.select(startdate)[0].get_text()
            print(startdate)
            if startdate_reg != "null":
                startdate = re.findall(eval(startdate_reg), startdate)[0]
                print(startdate)
    except Exception as e:
        print("startdate:" + str(e))

    try:
        if deadline == "":
            deadline = deadline_reg
        else:
            deadline = soup.select(deadline)[0].get_text()
            print(deadline)
            if deadline_reg != "null":
                deadline = re.findall(eval(deadline_reg), deadline)[0]
                print(deadline)
    except Exception as e:
        print("deadline:" + str(e))

    try:
        if tag == "":
            tag = tag_reg
        else:
            tag = soup.select(tag)[0].get_text()
            if tag_reg != "null":
                tag = re.findall(eval(tag_reg), tag)[0]
    except Exception as e:
        print("tag:" + str(e))

    try:
        if banner == "":
            banner = banner_reg
        else:
            banner = soup.select(banner)[0].get('src')
            print(banner)
            if website not in banner:
                banner = website + banner
            if banner_reg != "null":
                banner = re.findall(eval(banner_reg), tag)[0]
    except Exception as e:
        print("banner:" + str(e))
        banner = ""

    try:
        startdate, enddate = DateFormatHelper.convertStandardDateFormat(startdate)
        tmp = startdate.split("-")
        if len(tmp) == 3:
            startdate = datetime(int(tmp[0]), int(tmp[1]), int(tmp[2]))
    except:
        print("startdate")

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
    except:
        print("deadline")

    info_dict = {}
    info_dict["cnName"] = cnName
    info_dict["enName"] = enName
    info_dict["location"] = location
    info_dict["description"] = description
    info_dict["sponsor"] = sponsor
    if startdate != "":
        info_dict["startdate"] = startdate
    if enddate != "":
        info_dict["enddate"] = enddate
    if deadline != "":
        info_dict["deadline"] = deadline
    info_dict["website"] = website
    info_dict["tag"] = tag
    info_dict["banner"] = banner
    print(info_dict)
    return info_dict


if __name__ == '__main__':
    # configFileNames = getFileNames('file/configreg/')
    configFileNames = ["file/configreg/website2.conf"]
    conferences = []
    for item in configFileNames:
        print(item)
        info_dict = get_info(item)
        conferences.append(info_dict)



    # fields = ["cnName", "enName", "website", "tag", "banner",
    #               "location", "sponsor", "startdate", "enddate",
    #               "deadline", "description"]
    # table_str = "ConferenceInfo"
    # # conferences = readDictionary(fileName)
    # # date1 = dt.date.today()
    # b = str(Mysql.queryData("select website from ConferenceInfo"))
    # print(b)
    # for element in conferences:
    #     website = element.get('website')
    #     print(website)
    #     if website not in b:
    #         Mysql.saveObject(element, table_str, fields)
    #     else:
    #         Mysql.mysql_update(element, table_str, fields, website)
