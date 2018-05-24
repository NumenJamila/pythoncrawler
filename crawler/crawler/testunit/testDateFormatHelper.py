import json
import unittest
import sys

from datetime import date, datetime

from crawler.spider.logmanage import loadLogger
from crawler.util.fileoperate import readDictionary
from crawler.util.formathelper import DateFormatHelper, Conference
from crawler.util.mongodbhelper import MongoDBCRUD


def saveObject(obj: object):

    """
    删除字典中值为None的字典项
    :param obj:
    """
    dic = obj.__dict__
    keys = list(dic.keys())
    for k in keys:
        if dic.get(k) is None:
            dic.pop(k)
    for k, v in dic.items():
        print("key:\t{}\nvalue:\t{}\n".format(k, v))


class TestFormatApi(unittest.TestCase):
    def setUp(self):
        self.logger = loadLogger('applogconfig.ini')

    def testConvertEnglishFormat(self):
        helper = DateFormatHelper()
        pintstr = "17 Jun 2019"
        helper.convertStandardDateFormat(pintstr)

    def testOverloadConstructor(self):
        dic1 = {"enName": "OCEANS 2019 -  Marseille",
                "startdate": "17-20 Jun 2019",
                "website": "https://www.aconf.org/conf_70573.html",
                "enddate": "20 Jun 2019", "location": "Marseille, France Ain  .  France",
                "tag": "Engineering, Computing & Technology"
                }

        dic2 = {"enName": "OCEANS 2019 -  Marseille",
                "startdate": "17-20 Jun 2019",
                "website": "https://www.aconf.org/conf_70573.html",
                "enddate": "20 Jun 2019", "location": "Marseille, France Ain  .  France",
                "tag": "Engineering, Computing & Technology"
                }
        info1 = Conference(dic1)
        info2 = Conference(dic2)
        print("info1 == info2 = {}".format(info1 == info2))
        s = set()
        s.add(info1)
        s.add(info2)
        s2 = set()
        s2.add(info1)
        print("s-s2 = {}".format(s - s2))

    def testMergeExtractInfo(self):
        recordlist = readDictionary("../file/log/result.json")
        print("数据总数为:\t{0}".format(len(recordlist)))
        for i in range(0, len(recordlist)):
            dic = dict(recordlist[i])
            # print("\ndict:\t{}\n".format(dic))
            queue = DateFormatHelper.logqueue
            try:
                startdate = dic.get("startdate")
                startdate = DateFormatHelper.convertStandardDateFormat(startdate)
                tmp = startdate.split("-")
                if len(tmp) == 3:
                    startdate = datetime(int(tmp[0]), int(tmp[1]), int(tmp[2]))
                dic["startdate"] = startdate

                enddate = dic.get("enddate")
                enddate = DateFormatHelper.convertStandardDateFormat(enddate)
                tmp = enddate.split("-")
                if len(tmp) == 3:
                    enddate = datetime(int(tmp[0]), int(tmp[1]), int(tmp[2]))
                dic["enddate"] = enddate
                # Conference用于set去重
                MongoDBCRUD.insert(dic, "conference")
                print("ok")
            except Exception as e:
                print("异常信息：\t{}".format(sys.exc_info()))
                queue.put("\ncatch Exception:\t{}\n".format(e))
                continue

            # 写日志
            while not queue.empty():
                self.logger.debug(queue.get())
                # c = Conference(dic)
                # dic1 = {}
                # dic1.update(c.__dict__)
                # jsonstr = json.dumps(dic1, ensure_ascii=False)
                # print(jsonstr)

    def testQueryFromMongoDB(self):
        datas = MongoDBCRUD.query("conference", {}, {"cnName": 1, "enName": 1, "website": 1, "_id": 0, "startdate": 1},
                                  0, 1000)
        print(type(datas[0]))
        # for data in datas:
        #     print(data)
        datas = MongoDBCRUD.query("conference", {}, {}, 0, 1000)

    def testObjectdict(self):
        dic1 = {"enName": "OCEANS 2019 -  Marseille",
                "startdate": "17-20 Jun 2019",
                "website": "https://www.aconf.org/conf_70573.html",
                "enddate": "20 Jun 2019", "location": "Marseille, France Ain  .  France",
                "tag": "Engineering, Computing & Technology"
                }
        c = Conference(dic1)
        d = c.__dict__
        saveObject(c)
        # for i in d.keys():
        #     print("key:\t{}\nvalue:\t{}\n".format(i, d.get(i)))
