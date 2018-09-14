import re
from bs4 import BeautifulSoup

from pyquery import PyQuery as Pq

from .crawluritabledao import CrawledURLDao
from .fileoperate import *
from .mysqlhelper import Mysql
from .urllibhelper import SpiderApi
from multiprocessing import Process
from multiprocessing import Queue


def initConfigForm(form: dict) -> dict:
    """
    解析*.conf配置文件[post_data]部分的表单
    :param form: 从*.conf读取的配置文件信息，以字典的方式存储
    :return: 解析后的字典
    """
    for key in form.keys():
        v = str(form.get(key))
        # 将配置文件里的"{}"表达式解析为list对象
        if v.count("{") + v.count("}") >= 2 and v.startswith("{"):
            v = v[1:-1]  # 去除字符串第1个字符和最后1个字符
            if v.count(",") > 0:
                array = v.split(",")
                form[key] = array
            elif v.count("-") > 0:
                scope = v.split("-")
                array = []
                for i in range(int(scope[0]), int(scope[1]) + 1):
                    array.append(i)
                form[key] = array
    return form


def pageParsing(cfg: dict, form=None, filename=None):
    if filename is not None:
        removeFile(filename)
    writeToFile(filename, '[\n')
    baseurl = str(cfg.get("base_url"))
    way = cfg.get("way")
    index = 1
    end = 0
    innerindex = 0
    if cfg.get("begin") != 'null':
        index = int(cfg.get("begin"))
    if cfg.get("end") != 'null':
        end = int(cfg.get("end"))
    primaryInfo = []
    while index <= end:
        url = baseurl.format(index)
        print("http for url = {}".format(url))
        if way == 'get':
            html = SpiderApi.getPageSourceCode(url)
        else:
            form = initConfigForm(form)
            form_data = {}
            for key, val in form.items():
                if isinstance(val, list):
                    form_data[key] = val[innerindex]
                else:
                    form_data[key] = val
            print(form_data)
            cookieEntry = str(cfg.get("cookie")).split('=')
            cookie = {cookieEntry[0]: cookieEntry[1]}
            if cookie != 'null':
                html = SpiderApi.getPageSourceCodeByPost(url, form_data, cookie)
            else:
                html = SpiderApi.getPageSourceCodeByPost(url, form_data)
            innerindex += 1
        primaryInfo += extractPrimaryInfoByPQuery(html, cfg)
        index += 1
    length = len(primaryInfo)  # 获取抓取的会议信息条数
    i = 0
    # 把会议信息以json格式保存到文件文件里
    for t in primaryInfo:
        # 配置文件conf里的profix若为null表示待获取的url为完整的url
        # 若不为null，则为相对路径
        if str(cfg.get('profix')) != 'null':
            getConferenceUrl(t, cfg.get('profix'))
        writeToJson(t, filename)
        if i != length - 1:
            writeToFile(filename, ',\n')
        i += 1
    writeToFile(filename, '\n]')


def extractPrimaryInfoByPQuery(html: str, cfg: dict):
    html = getHtmlCore(html)
    doc = Pq(html)
    selector = cfg.get("tableselector")
    rowselector = cfg.get("rowselector")
    href = int((cfg.get("href"))) if cfg.get("href") != "null" else None
    cnname = int((cfg.get("cnname"))) if cfg.get("cnname") != "null" else None
    enname = int((cfg.get("enname"))) if cfg.get("enname") != "null" else None
    tag = int((cfg.get("tag"))) if cfg.get("tag") != "null" else None
    location = int((cfg.get("location"))) if cfg.get("location") != "null" else None
    sponsor = int((cfg.get("sponsor"))) if cfg.get("sponsor") != "null" else None
    startdate = int((cfg.get("startdate"))) if cfg.get("startdate") != "null" else None
    enddate = int((cfg.get("enddate"))) if cfg.get("enddate") != "null" else None
    deadline = int((cfg.get("deadline"))) if cfg.get("deadline") != "null" else None
    acceptance = int((cfg.get("acceptance"))) if cfg.get("acceptance") != "null" else None
    table = doc(selector)
    doc = Pq(str(table))
    rows = doc(rowselector)
    rowsoup = BeautifulSoup(str(rows), "lxml")
    rows = rowsoup.select(rowselector)  # 得到1个包含表格每行的list集合
    keyinfo = []
    for row in rows:
        index = 0
        mapper = {}
        xxx = []
        for cell in row.children:
            cellstr = str(cell)
            if cellstr != '\n' and len(cellstr) > 8:
                xxx.append(cellstr)
                soup = BeautifulSoup(cellstr, "lxml")
                if index == href:
                    a = soup.find("a")
                    if a is not None:
                        mapper["website"] = a.get("href")
                if index == cnname:
                    mapper["cnname"] = str(soup.get_text()).strip().replace("\t", "")
                elif index == enname:
                    mapper["enname"] = str(soup.get_text()).strip().replace("\t", "")
                elif index == tag:
                    mapper["tag"] = str(soup.get_text()).strip().replace("\t", "")
                elif index == location:
                    mapper["location"] = str(soup.get_text()).strip().replace("\t", "")
                elif index == sponsor:
                    mapper["sponsor"] = str(soup.get_text()).strip().replace("\t", "")
                elif index == startdate:
                    # 对英文网站特殊的日期格式进行特殊处理，提取日期
                    if str(cfg.get("language")) == 'en' and str(cfg.get("dateformat")) != 'null':
                        pattern = re.compile(str(cfg.get("dateformat")))
                        # pattern = re.compile(r'[0-9]{1,2}-[0-9]{1,2} *\w{3} *[0-9]{4}')
                        dates = pattern.findall(soup.get_text())
                        if len(dates) > 0:
                            mapper["startdate"] = str(dates[0])
                    else:
                        mapper["startdate"] = str(soup.get_text()).strip().replace("\t", "")
                elif index == enddate:
                    mapper["enddate"] = str(soup.get_text()).strip().replace("\t", "")
                elif index == deadline:
                    mapper["deadline"] = str(soup.get_text()).strip().replace("\t", "")
                elif index == acceptance:
                    mapper["acceptance"] = str(soup.get_text()).strip().replace("\t", "")
                index += 1
        keyinfo.append(mapper)
    return keyinfo


def getHtmlCore(html: str) -> str:
    """
    提取html源码里含有待提取信息的html源码
    :param html:
    """
    sources = html.split("</html>")
    maxindex = 0
    maxlen = 0
    maxblock = ""
    for i in range(len(sources)):
        if len(sources[i]) >= maxlen:
            maxlen = len(sources[i])
            maxindex = i
    maxblock = str(sources[maxindex]) + '</html>'
    soup = BeautifulSoup(maxblock, 'lxml')
    return maxblock


def getConferenceUrl(dic: dict, profix=None):
    if dic.get('website') is not None:
        url = str(dic.get('website'))
        if not url.startswith('http'):
            if profix is not None:
                url = profix + url
                dic['website'] = url


class HtmlCodeHandler(Process):
    def __init__(self, configfile, savefile, processname, logqueue: Queue):
        super().__init__()
        self.name = processname  # 进程名
        self.cfgfile = configfile  # 配置文件名
        self.savefile = savefile  # 抓取数据后保存的文件名，以.json为扩展名
        self.logqueue = logqueue
        self.cfglist = readConfig(configfile)  # 读取的*.conf配置文件字典
        self.cfg = self.cfglist[0]  # *.conf配置文件中第1节的配置信息

    @staticmethod
    def getInstance(configfile, savefile):
        handler = HtmlCodeHandler(configfile, savefile, "test_process", Queue())
        return handler

    def run(self):
        if len(self.cfglist) > 2:
            self.pageParsing(self.cfg, self.cfglist[1], self.savefile)
        else:
            self.pageParsing(self.cfg, filename=self.savefile)

    def initConfigForm(self, form: dict) -> dict:
        """
        解析*.conf配置文件[post_data]部分的表单
        :param form: 从*.conf读取的[post_data]节下配置文件信息，以字典的方式存储
        :return: [post_data]节配置信息解析后的字典
        """
        for key in form.keys():
            v = str(form.get(key))
            # 将配置文件里的"{}"表达式解析为list对象
            if v.count("{") + v.count("}") >= 2 and v.startswith("{"):
                v = v[1:-1]  # 去除字符串第1个字符和最后1个字符
                if v.count(",") > 0:
                    array = v.split(",")
                    form[key] = array
                elif v.count("-") > 0:
                    scope = v.split("-")
                    array = []
                    for i in range(int(scope[0]), int(scope[1]) + 1):
                        array.append(i)
                    form[key] = array
        return form

    def getHtmlCore(self, html: str) -> str:
        """
        提取html源码里含有待提取信息的html源码
        :param html:
        """
        sources = html.split("</html>")
        maxindex = 0
        maxlen = 0
        maxblock = ""
        for i in range(len(sources)):
            if len(sources[i]) >= maxlen:
                maxlen = len(sources[i])
                maxindex = i
        maxblock = str(sources[maxindex]) + '</html>'
        return maxblock

    def pageParsing(self, cfg: dict, form=None, filename=None):
        """

        :param cfg: *.conf配置文件中第1节下的字典
        :param form: post请求需要的表单数据，不填默认为get
        :param filename: 抓取的目标信息保存的地方，以.json扩展名保存
        """
        if filename is not None:
            removeFile(filename)
        writeToFile(filename, '[\n')
        baseurl = str(cfg.get("base_url"))
        way = cfg.get("way")
        index = 1
        end = 0
        innerindex = 0
        if cfg.get("begin") != 'null':
            index = int(cfg.get("begin"))
        if cfg.get("end") != 'null':
            end = int(cfg.get("end"))
        primaryInfo = []
        while index <= end:
            try:
                url = baseurl.format(index)
                print("http for url = {}".format(url))
                if way == 'get':
                    html = SpiderApi.getPageSourceCode(url)
                else:
                    form = self.initConfigForm(form)
                    form_data = {}
                    for key, val in form.items():
                        if isinstance(val, list):
                            form_data[key] = val[innerindex]
                        else:
                            form_data[key] = val
                    print(form_data)
                    cookieEntry = str(cfg.get("cookie")).split('=')
                    cookie = {cookieEntry[0]: cookieEntry[1]}
                    if cookie != 'null':
                        html = SpiderApi.getPageSourceCodeByPost(url, form_data, cookie)
                    else:
                        html = SpiderApi.getPageSourceCodeByPost(url, form_data)
                    innerindex += 1
                primaryInfo += self.extractPrimaryInfoByPQuery(html, cfg)
            except Exception as e:
                self.logqueue.put('\n异常信息：{}\n '.format(e))
            finally:
                index += 1

        crawlUrlMap = dict()

        for t in primaryInfo:
            # 配置文件conf里的profix若为null表示待获取的url为完整的url
            # 若不为null，则为相对路径
            if str(cfg.get('profix')) != 'null':
                self.getConferenceUrl(t, cfg.get('profix'))
            url = dict(t).get('website')
            if url:
                crawlUrlMap[url] = t
        i = 0
        length = len(crawlUrlMap)  # 获取未被解析的URL数目
        # 把未被解析的URL会议信息以json格式保存到文件里
        for value in crawlUrlMap.values():
            writeToJson(value, filename)
            if i != length - 1:
                writeToFile(filename, ',\n')
            i += 1
        writeToFile(filename, '\n]')


    def extractPrimaryInfoByPQuery(self, html: str, cfg: dict):
        html = self.getHtmlCore(html)
        doc = Pq(html)
        selector = cfg.get("tableselector")
        rowselector = cfg.get("rowselector")
        href = int((cfg.get("href"))) if cfg.get("href") != "null" else None
        cnname = int((cfg.get("cnname"))) if cfg.get("cnname") != "null" else None
        enname = int((cfg.get("enname"))) if cfg.get("enname") != "null" else None
        tag = int((cfg.get("tag"))) if cfg.get("tag") != "null" else None
        location = int((cfg.get("location"))) if cfg.get("location") != "null" else None
        sponsor = int((cfg.get("sponsor"))) if cfg.get("sponsor") != "null" else None
        startdate = int((cfg.get("startdate"))) if cfg.get("startdate") != "null" else None
        enddate = int((cfg.get("enddate"))) if cfg.get("enddate") != "null" else None
        deadline = int((cfg.get("deadline"))) if cfg.get("deadline") != "null" else None
        acceptance = int((cfg.get("acceptance"))) if cfg.get("acceptance") != "null" else None
        table = doc(selector)
        doc = Pq(str(table))
        rows = doc(rowselector)
        rowsoup = BeautifulSoup(str(rows), "lxml")
        rows = rowsoup.select(rowselector)  # 得到1个包含表格每行的list集合
        keyinfo = []
        for row in rows:
            index = 0;mapper = {};xxx = []
            for cell in row.children:
                cellstr = str(cell)
                if cellstr != '\n' and len(cellstr) > 8:
                    xxx.append(cellstr)
                    soup = BeautifulSoup(cellstr, "lxml")
                    if index == href:
                        a = soup.find("a")
                        if a is not None:
                            mapper["website"] = a.get("href")
                    if index == cnname:
                        mapper["cnName"] = str(soup.get_text()).strip().replace("\t", "")
                    elif index == enname:
                        s = str(soup.get_text()).strip().replace("\t", "")
                        ii = s.find("\n")
                        if ii != -1:
                            mapper["enName"] = s[0: ii]
                        else:
                            mapper["enName"] = s
                    elif index == tag:
                        mapper["tag"] = str(soup.get_text()).strip().replace("\t", "")
                    elif index == location:
                        mapper["location"] = str(soup.get_text()).strip().replace("\t", "")
                    elif index == sponsor:
                        mapper["sponsor"] = str(soup.get_text()).strip().replace("\t", "")
                    elif index == startdate:
                        # 对英文网站特殊的日期格式进行特殊处理，提取日期
                        if str(cfg.get("language")) == 'en' and str(cfg.get("dateformat")) != 'null':
                            pattern = re.compile(str(cfg.get("dateformat")))
                            # pattern = re.compile(r'[0-9]{1,2}-[0-9]{1,2} *\w{3} *[0-9]{4}')
                            dates = pattern.findall(soup.get_text())
                            if len(dates) > 0:
                                mapper["startdate"] = str(dates[0])
                        else:
                            mapper["startdate"] = str(soup.get_text()).strip().replace("\t", "")
                    elif index == enddate:
                        mapper["enddate"] = str(soup.get_text()).strip().replace("\t", "")
                    elif index == deadline:
                        mapper["deadline"] = str(soup.get_text()).strip().replace("\t", "")
                    elif index == acceptance:
                        mapper["acceptance"] = str(soup.get_text()).strip().replace("\t", "")
                    index += 1
            keyinfo.append(mapper)
        return keyinfo

    def getConferenceUrl(self, dic: dict, profix=None):
        if dic.get('website') is not None:
            url = str(dic.get('website'))
            if not url.startswith('http'):
                if profix is not None:
                    url = profix + url
                    dic['website'] = url
