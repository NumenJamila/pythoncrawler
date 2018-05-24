import random
import unittest

import jieba.analyse
import jieba.posseg

from crawler.spider.subpagehandle import parseSubPage, readKeywordCongig
from crawler.util.fileoperate import readConfig, readDictionary, readSectionsInConfig
from multiprocessing import Queue


class TestMethodsInSubPageHandleModule(unittest.TestCase):
    def setUp(self):
        self.keyfile = "../file/config/keyword5.txt"
        filename = "../file/config/website5.conf"
        name = '../file/log/5.json'
        self.logqueue = Queue()
        self.itemqueue = Queue()
        # 读取配置文件
        dicList = readConfig(filename)
        # 获取网站域名
        self.domainname = readSectionsInConfig(filename)[0]
        dicts = readDictionary(name)  # 获取从会议网站初次抓取的信息
        index = random.randint(0, len(dicts) - 1)
        self.keydic = dicts[index]  # 随机抽取1条从会议网站抓取的信息以字典的方式保存
        if len(dicList) > 2:
            self.firstcfg = dict(dicList[0])  # 读取配置文件第1节配置信息
            self.subpagecfg = dict(dicList[2])  # 读取配置文件第3节子页配置信息
        else:
            self.firstcfg = dict(dicList[0])  # 读取配置文件第1节配置信息
            self.subpagecfg = dict(dicList[1])  # 读取配置文件第3节子页配置信息
        print('待测试URL：\n{}'.format(dicts[index]))
        print('网站域名：{}'.format(self.domainname))

    def testFuncParseSubPage(self):
        keywordConfigMap = readKeywordCongig(self.keyfile)
        keywordmap = keywordConfigMap[0]
        othermap = keywordConfigMap[1]
        parseSubPage(self.subpagecfg, self.keydic, self.domainname,
                     "process1", keywordmap, othermap)


class TestJiebaExtractor(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def testExtracteTag(self):
        # string = "第一届阿拉伯自然语言处理国际研讨会"
        string = "14th International Conference on Intellectual Capital, Knowledge " \
                 "Management and Organisational Learning - ICICKM 2017"
        # string = "11th European Conference on Games based Learning - ECGBL 2017"
        cutword = jieba.posseg.cut(string)
        for w, flag in cutword:
            print("{}\t{}".format(w, flag))
        jieba.analyse.set_stop_words("../file/txt/stop_words.txt")
        words = jieba.analyse.extract_tags(string, 5)
        w = " ".join(words)
        print(type(words))
        print(w)
