import unittest

from crawler.spider.analysesources import initConfigForm, pageParsing
from crawler.util.fileoperate import readConfig, readDictionary


class TestMethodInFileOPerateModule(unittest.TestCase):
    def setUp(self):
        print("start test")

    def testReadconfig(self):
        """
        单元测试：
        测试函数：readConfig()
        测试函数：initConfigForm()
        """
        filename = "../file/config/website2.conf"
        dicList = readConfig(filename)
        for i in range(0, len(dicList)):
            print("- " * 50)
            dic = dicList[i]
            if i == 1:
                dic = initConfigForm(dic)
                print(dic)
            for key, value in dic.items():
                print("key = {k}, value = {v}".format(k=key, v=value))

    def testPageParsing1(self):
        filename = "../file/config/website1.conf"
        savename = '../file/log/1.json'
        dicList = readConfig(filename)
        if len(dicList) > 2:
            pageParsing(dicList[0], dicList[1], savename)
        else:
            pageParsing(dicList[0], filename=savename)

    def testPageParsing2(self):
        filename = "../file/config/website2.conf"
        savename = '../file/log/2.json'
        dicList = readConfig(filename)
        print(dicList)
        if len(dicList) > 2:
            pageParsing(dicList[0], dicList[1], savename)
        else:
            pageParsing(dicList[0], filename=savename)

    def testPageParsing3(self):
        filename = "../file/config/website3.conf"
        savename = '../file/log/3.json'
        dicList = readConfig(filename)
        print(dicList)
        if len(dicList) > 2:
            pageParsing(dicList[0], dicList[1], savename)
        else:
            pageParsing(dicList[0], filename=savename)

    def testPageParsing4(self):
        filename = "../file/config/website4.conf"
        savename = '../file/log/4.json'
        dicList = readConfig(filename)
        print(dicList)
        if len(dicList) > 2:
            pageParsing(dicList[0], dicList[1], savename)
        else:
            pageParsing(dicList[0], filename=savename)

    def testReadDictionary(self):
        name = '../file/log/3.json'
        dicts = readDictionary(name)
        for dic in dicts:
            print(dic)

    def testPageParsing5(self):
        filename = "../file/config/website5.conf"
        savename = '../file/log/5.json'
        dicList = readConfig(filename)
        print(dicList)
        if len(dicList) > 2:
            pageParsing(dicList[0], dicList[1], savename)
        else:
            pageParsing(dicList[0], filename=savename)
