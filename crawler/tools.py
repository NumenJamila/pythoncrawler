#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/8 15:23
# @Author  : ZengJunMing
# @File    : tools.py

import re
import random
import requests
import sys


class SpiderApi(object):
    user_agents = [
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/43.0.2357.134 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2595.400 QQBrowser/9.6.10872.400",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
        "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko)"
        "Chrome/18.0.1025.133 Mobile Safari/535.19"
    ]
    content_type = 'application/x-www-form-urlencoded'
    accept = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    referer = ""

    @classmethod
    def getRequestHeader(cls):
        header = {}
        header['User-Agent'] = cls.user_agents[random.randint(0, len(cls.user_agents) - 1)]
        header['Accept'] = cls.accept
        header['Content-Type'] = cls.content_type
        return header

    @classmethod
    def getBinContent(cls,url):
        headers = cls.getRequestHeader()
        content = requests.get(url, headers=headers)  # 返回一个Response对象
        print("状态码：{s}".format(s=content.status_code))
        return content

    @classmethod
    def getPageSourceCode(cls, url):
        headers = cls.getRequestHeader()
        html = ""
        try:
            start_html = requests.get(url, headers=headers)  # 返回一个Response对象
            print("状态码：{s}".format(s=start_html.status_code))
            start_html.raise_for_status()
            # response内容的编码
            header_code = start_html.encoding
            # response返回的html header标签里设置的编码
            html_header_code = requests.utils.get_encodings_from_content(start_html.text)
            if header_code == 'ISO-8859-1':
                if html_header_code:
                    html_header_code = html_header_code[0]
                else:
                    html_header_code = start_html.apparent_encoding
                encode_content = start_html.content.decode(html_header_code, 'replace').encode('utf-8', 'replace')
                html = encode_content.decode('utf-8')
            else:
                html = start_html.text
        except:
            print("class SpiderApi.getPageSourceCode()异常信息：{}".format(sys.exc_info()))
        finally:
            return html

    @classmethod
    def getPageSourceCodeByPost(cls, url, dictionary, cookie=None):
        html = ""
        headers = cls.getRequestHeader()
        try:
            if cookie is not None:
                html = requests.post(url, data=dictionary, headers=headers, cookies=cookie)
            else:
                html = requests.post(url, data=dictionary, headers=headers)
            print("状态码：{s}".format(s=html.status_code))
            html.raise_for_status()  # 响应状态码大于400将抛出异常
            content_coding = html.encoding  # 获取响应报文数据部分编码
            # 获取html页面里设置的编码
            page_encoding = requests.utils.get_encodings_from_content(html.text)
            if content_coding == 'ISO-8859-1':
                if page_encoding is not None:
                    page_encoding = page_encoding[0]
                else:
                    page_encoding = html.apparent_encoding
                    encoding_content = html.content.decode(page_encoding, 'replace').encode('utf-8', 'replace')
                    html = encoding_content.decode('utf-8')
            else:
                html = html.text
        except:
            print("异常信息：{exception}".format(exception=sys.exc_info()))
        return html


class DateFormatHelper(object):
    regex1 = re.compile(r"[0-9]{1,2}-[0-9]{1,2} *[A-Za-z]+ *[0-9]{4}")
    regex2 = re.compile(r"[0-9]{1,2} *[A-Za-z]+ *[0-9]{4}")
    regex3 = re.compile(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}")
    regex4 = re.compile(r"[A-Za-z]+ *[0-9]{1,2}, *[0-9]{4}")
    regex5 = re.compile(r"[A-Za-z]+ *[0-9]{1,2}-[0-9]{1,2}, *[0-9]{4}")
    regex6 = re.compile(r"[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日")
    dateformatregexs = [regex1, regex2, regex3, regex4, regex5, regex6]

    monthMap = {"sep": "9", "oct": "10", "nov": "11", "dec": "12", "jan": "1", "feb": "2",
                "aug": "8", "jul": "7", "jun": "6", "may": "5", "apr": "4", "mar": "3"}
    monthMap2 = {"September": "9", "October": "10", "November": "11", "December": "12",
                 "January": "1", "February": "2", "August": "8", "July": "7",
                 "June": "6", "May": "5", "April": "4", "March": "3"}
    monthMap = {"sep.": "9", "oct.": "10", "nov.": "11", "dec.": "12", "jan.": "1", "feb.": "2",
                "aug.": "8", "jul.": "7", "jun.": "6", "may.": "5", "apr.": "4", "mar.": "3"}
    @classmethod
    def convertStandardDateFormat(cls, datestr: str) -> str:
        """
        转换日期格式
        :param datestr:
        :return:
        """
        res = ""
        res2 = ""
        if datestr is None:
            return res, res2
        for i in range(0, len(cls.dateformatregexs)):
            try:
                regex = cls.dateformatregexs[i]
                match = regex.match(datestr)
                if match is not None:
                    itemstr = match.group()
                    if i == 0:
                        items = str(itemstr).split(" ")
                        year = items[len(items) - 1]
                        month = cls.monthMap.get(str(items[1]).lower())
                        if month is None:
                            month = cls.monthMap2.get(str(items[1]))
                        dayrange = str(items[0])
                        day = dayrange[0:dayrange.index("-")]
                        day2 = dayrange[dayrange.index("-") + 1:dayrange.index(",")]
                        res = year + "-" + month + "-" + day
                        res2 = year + "-" + month + "-" + str(day2)
                    elif i == 1:
                        items = str(itemstr).split(" ")
                        year = items[len(items) - 1]
                        month = cls.monthMap.get(str(items[1]).lower())
                        if month is None:
                            month = cls.monthMap2.get(str(items[1]))
                        day = items[0]
                        res = year + "-" + month + "-" + day
                    elif i == 3:
                        items = str(itemstr).split(" ")
                        year = items[len(items) - 1]
                        month = cls.monthMap.get(str(items[0]).lower())
                        if month is None:
                            month = cls.monthMap2.get(str(items[0]))
                        digit_pattern = re.compile(r'[0-9]+')
                        digitlist = digit_pattern.findall(items[1])
                        day = digitlist[0]
                        res = year + "-" + month + "-" + day
                    elif i == 4:
                        items = str(itemstr).split(" ")
                        year = items[len(items) - 1]
                        month = cls.monthMap.get(str(items[0]).lower())
                        if month is None:
                            month = cls.monthMap2.get(str(items[0]))
                        dayrange = str(items[1])
                        day = dayrange[0:dayrange.index("-")]
                        day2 = dayrange[dayrange.index("-")+1:dayrange.index(",")]
                        res = year + "-" + month + "-" + day
                        res2 = year + "-" + month + "-" + day2
                    elif i == 5:
                        for x in range(len(str(itemstr))):
                            if ord(itemstr[x]) > 255:
                                itemstr = itemstr.replace(itemstr[x], " ")
                        items = str(itemstr).split(" ")
                        year = items[0]
                        month = items[1]
                        day = items[2]
                        res = year + "-" + month + "-" + day
                    else:
                        res = datestr
                    print(res)
                    break
            except Exception as e:
                print("convertStandardDateFormat方法出现异常{}".format(e))
        return res, res2
