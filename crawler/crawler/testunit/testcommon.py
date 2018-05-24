import unittest

from crawler.model.testmodel import Person
from crawler.service.taghanldler import NPExtractor
from crawler.util.formathelper import Conference
from crawler.util.mysqlhelper import Mysql


class CommonTest(unittest.TestCase):
    def referenceParamPro(self, currentset: set):
        print("currentset.size = {}".format(len(currentset)))
        person3 = Person("WangWu", 19)
        s = set()
        s.add(person3)
        currentset = currentset - s
        currentset.clear()
        print("currentset.size = {}".format(len(currentset)))

    def setUp(self):
        super().setUp()
        print("start")

    def testClass(self):
        person1 = Person("Zhangsan", 19)
        person2 = Person("Zhangsan", 20)
        person3 = Person("Zhangsan", 19)

        print("person1 == person2 = {}".format(person1 == person2))
        print("person1 == person3 = {}".format(person1 == person3))

    def testClassSet1(self):
        person1 = Person("Zhangsan", 19)
        person2 = Person("Lisi", 20)
        person3 = Person("WangWu", 19)
        s = set()
        s.add(person1)
        s.add(person2)
        s.add(person3)

        print("before call referenceParamPro():set.length = {}".format(len(s)))

        self.referenceParamPro(s)
        print("after call referenceParamPro():set.length = {}".format(len(s)))

    def testClassSet2(self):
        person1 = Person("Zhangsan", 19)
        person2 = Person("Lisi", 20)
        person3 = Person("WangWu", 19)
        s = set()
        s.add(person1)
        s.add(person2)
        s.add(person3)

        print("before call clear():set.length = {}".format(len(s)))

        s.clear()
        print("after call clear():set.length = {}".format(len(s)))

    def testClassVariable(self):
        print("1. Person.count = {}".format(Person.count))
        person1 = Person("Zhangsan", 19)
        Person.count = 1
        print("2. Person.count = {}".format(Person.count))
        person2 = Person("WangWu", 19)
        Person.setCount(3)
        person3 = Person("aqian", 22)
        person3.getCountValue()

    def testObjectDictionary(self):
        mapper = {"startdate": "2017-12-16", "website": "http://www.icmite.org",
                  "location": "成都",
                  "cnName": "2017 第3届机械,电子与信息技术工程国际会议(ICMITE2017,EI收录)"}

        conference = Conference(mapper)
        dic = conference.__dict__
        fieldlist = ["cnName", "enName", "website", "tag",
                     "location", "sponsor", "startdate", "enddate",
                     "deadline", "acceptance"]
        fieldset = set(fieldlist)
        itemdic = fieldset & dic.keys()
        for k in itemdic:
            print("key= {}\tvalue=  {}".format(k, dic.get(k)))

    def testQueryStopWords(self):
        stopwordsql = "select word from JiebaStopWord"
        rows = Mysql.queryData(stopwordsql)
        f = lambda tup: tup[0] if tup else ""
        result = map(f, rows)
        string = "\n".join(result)
        print(string)
        print("set = {}".format(set(string.split("\n"))))

    def testQueryKeywords2TagMap(self):
        keywords_map_tag_sql = "select `name`,directionName from ResearchDirection,Tags " \
                               "where rdid = directionId"

        keyword2tagtuple = Mysql.queryData(keywords_map_tag_sql)
        keyword2tagmap = {}
        for tup in keyword2tagtuple:
            keyword2tagmap[tup[0]] = tup[1]
        for k, v in keyword2tagmap.items():
            print("key = {}\tvalue = {}".format(k, v))

    def testNPExtractor(self):
        sentence = "EuCAP 2018 : The 12th European Conference on Antennas and Propagation"
        keywords = NPExtractor.extractKeywords(sentence)
        print("\n".join(keywords))
