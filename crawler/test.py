#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/20 12:55
# @Author  : ZengJunMing
# @File    : test.py
"""
爬取ccf历史会议信息（可删）

"""
from crawler.util.fileoperate import *
from crawler.spider.analysesources import HtmlCodeHandler
from crawler.spider.subpagehandle import readKeywordCongig, parseSubPage
from crawler.spider.analysesources import *
a = None
if a is None:
    print(a+"为空")
else:
    print(a+"不为空")
# from crawler.util.mysqlhelper import Mysql
# import datetime
# # from main import *
# date1 = datetime.date.today() + datetime.timedelta(days=3)
# date2 = date1 + datetime.timedelta(days=6)
# print(date2)
# a = Mysql.queryData("select * from ConferenceInfo where startdate >= %s and startdate <= %s", params=(date1, date2))
# for item in a:
#     print(item)
#
# fields = ["cnName", "enName", "website", "tag", "description",
#               "location", "sponsor", "startdate", "enddate",
#               "deadline"]
# table_str = "ConferenceInfo"
# conferences = [{'cnName': '', 'enName': '', 'Location': '', 'description': {'info1': '这是一个大数据时代，它正以一种全新的生产方式改变着世界。随着大数据分析\xa0市场快速渗透到各行各业，哪些大数据技术是刚需?哪些技术有极大的潜在价值?我们诚挚邀请您参加\xa02018年大数据科技国际会议（ICBDT2018）,该会议于\xa02018年5月18-20日\xa0在\xa0中国·杭州\xa0举办，为期三天，以时下热门主题"大数据技术"为主题，期待您的到来！','info2': '100'}, 'sponsor': '', 'startdate': datetime.datetime(2018, 5, 18, 0, 0), 'enddate': '', 'deadline': datetime.datetime(2018, 3, 25, 0, 0), 'website': 'http://www.icbdt.org/', 'tag': ''}]
# for element in conferences:
#     Mysql.saveObject(element, table_str, fields)
#     print(element)
# d = Mysql.deleteById()

# b = Mysql.queryData("select * from ConferenceInfo where startdate >= %s", params=date1)
# for item in b:
#      print(item)

# cfglist = readConfig("file/config//website1.conf")
# cfg = cfglist[0]
# baseurl = str(cfg.get("base_url"))
# html = SpiderApi.getPageSourceCode(baseurl)
# soup = BeautifulSoup(html, "lxml")
# hrefs = soup.find_all("ul", attrs={"class": "g-ul m-snv"})
# info = []
# href_dict = {}
#
# for href in hrefs:
#     h = href.find_all("li")
#
# fileName = "file/log/1.json"
# removeFile(fileName)
# writeToFile(fileName, "[\n")
# base_urls = []
# tag_name = []
# tag_all = []
# for i in h:
#     website = "http://www.ccf.org.cn" + i.a["href"]
#     base_urls.append(website)
#     tag1 = i.get_text()
#     tag_name.append(tag1)
#
# tag_list = ["A", "B", "C"]
#
# print(base_urls)
# index = 1
# for url in base_urls[1:10]:
#     html2 = SpiderApi.getPageSourceCode(url)
#     soup1 = BeautifulSoup(html2, "lxml")
#     for m in range(3, 6):
#         soup2 = soup1.find_all("div", attrs={"class": "main m-b-md"})[0].find_all("div")[5].find_all("ul")[m]
#
#         soup3 = soup2.find_all("li")
#         for x in soup3[1:]:
#             enName = x.find_all("div")[2].string
#             sponsor = x.find_all("div")[3].string
#             website = x.find_all("div")[4].string
#             tag = "ccf-" + tag_list[m-3] + "," + tag_name[index]
#             tag_all.append(tag)
#             tag_all.append(tag_name[index])
#             href_dict["enName"] = enName
#             href_dict["sponsor"] = sponsor
#             href_dict["website"] = website
#             href_dict["tag"] = ",".join(tag_all)
#             info.append(href_dict)
#             href_dict = {}
#             tag_all = []
#             print(enName, sponsor, website)
#             print(website)
#     index += 1
# print(tag_all)
# length = len(info)
# i = 0
# for value in info:
#     writeToJson(value, fileName)
#     if i != length - 1:
#         writeToFile(fileName, ',\n')
#     i += 1
# writeToFile(fileName, '\n]')

# fields = ["cnName", "enName", "website", "tag",
#               "location", "sponsor", "startdate", "enddate",
#               "deadline", "acceptance"]
# table_str = "ConferenceInfo"
# conferences = readDictionary(fileName)
# for element in conferences:
#     Mysql.saveObject(element, table_str, fields)
#     print(element)



