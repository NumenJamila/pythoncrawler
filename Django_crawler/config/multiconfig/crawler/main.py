import datetime

from .fileoperate import *
from .analysesources import HtmlCodeHandler
from .subpagehandle import readKeywordCongig, parseSubPage
from multiprocessing import Pool
import sys
from .logmanage import loadLogger
from .conferenceDao import saveConferenceSet
from .conferenceDao import updateConferenceSet
from multiprocessing import Queue

from .mysqlhelper import Mysql
from .typeconverter import Converter
from .extractkeyword import get_info
from . import configsetting as cs
itemqueue = Queue()
def put(dic: dict):
    global itemqueue
    if len(dic) > 2:
        itemqueue.put(dic)


def showDict(dic: dict):
    print("callback -----> {}".format(dic))


def checkresult(conf):
    # 清空日志内容
    # clearContent('multiconfig//crawler//debug.log')
    # clearContent('multiconfig//crawler//info.log')

    startTime = datetime.datetime.now()
    confConfigFileNames = [conf.confConfigFileNames]
    txtConfigFileNames = [conf.txtConfigFileNames]
    # 加载日志配置文件
    logger = loadLogger('multiconfig/crawler/applogconfig.ini')
    # logger.info("主进程id为：\t{}".format(os.getpid()))

    savejsonfilenames = []  # 初次抓取的目标信息保存的路径

    # 生成初次爬取信息的临时文件名
    for i in range(1, len(confConfigFileNames) + 1):
        name = r'multiconfig/crawler/log/{}.json'.format(i)
        savejsonfilenames.append(name)
    processlist = []

    #  用于记录debug级别日志的队列
    debuglogqueue = Queue()

    # for i in range(0, 1):
    for i in range(0, len(confConfigFileNames)):
        processname = 'process{}'.format(i)
        sourcecodedealProcess = HtmlCodeHandler(confConfigFileNames[i],
                                                savejsonfilenames[i],
                                                processname, debuglogqueue)
        processlist.append(sourcecodedealProcess)
        sourcecodedealProcess.start()
    for p in processlist:
        p.join()
    # logger.info("所有子进程执行完")
    while not debuglogqueue.empty():
        logger.info(debuglogqueue.get())

    # itemdics为二维列表，每一个元素存放'file/log/*.json'里的字典
    itemdics = []
    for jsonfile in savejsonfilenames:
        try:
            jsonitem = readDictionary(jsonfile)
            itemdics.append(jsonitem)
        except Exception as e:
            print("Exception:\t{}".format(sys.exc_info()))

    # websiteConfInfos二维列表，每个元素保存的是websiteX.conf配置文件[协议://域名]和[sub_page]下的信息
    websiteConfInfos = []
    # websiteDomains存放着websiteX.conf配置文件[协议://域名]里的内容(X=1,2,3……)，
    # 比如有个配置文件里第一个为[http://meeting.sciencenet.cn]，
    # websiteDomains=[http://meeting.sciencenet.cn,……]
    websiteDomains = []
    for filename in confConfigFileNames:
        dicList = readConfig(filename)
        sections = readSectionsInConfig(filename)
        websiteDomains.append(sections[0])
        if len(dicList) > 2:
            firstcfg = dict(dicList[0])  # 读取配置文件第1节配置信息
            secondcfg = dict(dicList[2])  # 读取配置文件第3节子页配置信息
            websiteConfInfos.append([firstcfg, secondcfg])
        else:
            firstcfg = dict(dicList[0])  # 读取配置文件第1节配置信息
            secondcfg = dict(dicList[1])  # 读取配置文件第3节子页配置
            websiteConfInfos.append([firstcfg, secondcfg])

    resultFileName = r'multiconfig/crawler/result.json'
    removeFile(resultFileName)
    writeToFile(resultFileName, '[\n')


    # 查询所有停用的过滤词
    stopwordsql = "select word from JiebaStopWord"
    rows = Mysql.queryData(stopwordsql)

    # 将查询出来的元组转换为字符串和集合
    f = lambda tup: tup[0] if tup else ""
    maprows = map(f, rows)
    content = "\n".join(maprows)
    filterwords = set(content.split('\n'))
    # 将停用词写到 stop_words.txt 文件里
    writeToFile(r"multiconfig/crawler/stop_words.txt", content, pattern='w+')

    # 查询关键词到Tag的映射
    keywords_map_tag_sql = "select `name`,directionName from ResearchDirection,Tags " \
                           "where rdid = directionId"

    keyword2tagtuple = Mysql.queryData(keywords_map_tag_sql)
    keyword2tagmap = {}
    for tup in keyword2tagtuple:
        keyword2tagmap[tup[0]] = tup[1]

    # 创建进程池
    processpool = Pool(processes=4)
    
    # for i in range(0, 1):
    for i in range(0, len(websiteDomains)):
        domain = websiteDomains[i]
        confDictionary1 = websiteConfInfos[i][0]
        confDictionary2 = websiteConfInfos[i][1]
        keywordConfFile = txtConfigFileNames[i]
        params = readKeywordCongig(keywordConfFile)
        for j in range(0, len(itemdics[i])):
            processName = 'process{}'.format(j)
            # print("j = {}".format(j))
            processpool.apply_async(parseSubPage,
                                    (confDictionary2, itemdics[i][j], domain, processName,
                                     params[0], params[1], keyword2tagmap, filterwords),
                                    callback=put)
    processpool.close()
    processpool.join()
    currentset = set()  # 需要插入的信息对象集合
    presistenceset = set()  # 需要更新的信息对象集合
    b = str(Mysql.queryData("select website from " + cs.db_table))  # 根据网址决定是要插入还是更新
    while not itemqueue.empty():
        #  从队列中取出解析后会议信息字典
        info_dict = itemqueue.get()
        info_dict['taskname'] = conf.taskname
        writeToJson(info_dict, resultFileName)
        writeToFile(resultFileName, ',\n')
        info_dict = Converter.convert_dict_to_entry(info_dict)
        #  将Conference 对象添加到当前集合里
        currentset.add(info_dict)
    writeToFile(resultFileName, '\n{}\n]')
    finishTime = datetime.datetime.now()
    # logger.info("程序总共运行时间为 {}".format(finishTime - startTime))
    return currentset

def inputDB(conf):
    # # 清空日志内容
    # clearContent('multiconfig//crawler//debug.log')
    # clearContent('multiconfig//crawler//info.log')

    startTime = datetime.datetime.now()
    confConfigFileNames = [conf.confConfigFileNames]
    txtConfigFileNames = [conf.txtConfigFileNames]
    # 加载日志配置文件
    logger = loadLogger('multiconfig/crawler/applogconfig.ini')
    # logger.info("主进程id为：\t{}".format(os.getpid()))

    savejsonfilenames = []  # 初次抓取的目标信息保存的路径

    # 生成初次爬取信息的临时文件名
    for i in range(1, len(confConfigFileNames) + 1):
        name = r'multiconfig/crawler/log/{}.json'.format(i)
        savejsonfilenames.append(name)
    processlist = []

    #  用于记录debug级别日志的队列
    debuglogqueue = Queue()

    # for i in range(0, 1):
    for i in range(0, len(confConfigFileNames)):
        processname = 'process{}'.format(i)
        sourcecodedealProcess = HtmlCodeHandler(confConfigFileNames[i],
                                                savejsonfilenames[i],
                                                processname, debuglogqueue)
        processlist.append(sourcecodedealProcess)
        sourcecodedealProcess.start()
    for p in processlist:
        p.join()
    # logger.info("所有子进程执行完")
    while not debuglogqueue.empty():
        logger.info(debuglogqueue.get())

    # itemdics为二维列表，每一个元素存放'file/log/*.json'里的字典
    itemdics = []
    for jsonfile in savejsonfilenames:
        try:
            jsonitem = readDictionary(jsonfile)
            itemdics.append(jsonitem)
        except Exception as e:
            print("Exception:\t{}".format(sys.exc_info()))

    # websiteConfInfos二维列表，每个元素保存的是websiteX.conf配置文件[协议://域名]和[sub_page]下的信息
    websiteConfInfos = []
    # websiteDomains存放着websiteX.conf配置文件[协议://域名]里的内容(X=1,2,3……)，
    # 比如有个配置文件里第一个为[http://meeting.sciencenet.cn]，
    # websiteDomains=[http://meeting.sciencenet.cn,……]
    websiteDomains = []
    for filename in confConfigFileNames:
        dicList = readConfig(filename)
        sections = readSectionsInConfig(filename)
        websiteDomains.append(sections[0])
        if len(dicList) > 2:
            firstcfg = dict(dicList[0])  # 读取配置文件第1节配置信息
            secondcfg = dict(dicList[2])  # 读取配置文件第3节子页配置信息
            websiteConfInfos.append([firstcfg, secondcfg])
        else:
            firstcfg = dict(dicList[0])  # 读取配置文件第1节配置信息
            secondcfg = dict(dicList[1])  # 读取配置文件第3节子页配置
            websiteConfInfos.append([firstcfg, secondcfg])

    resultFileName = r'multiconfig/crawler/result.json'
    removeFile(resultFileName)
    writeToFile(resultFileName, '[\n')


    # 查询所有停用的过滤词
    stopwordsql = "select word from JiebaStopWord"
    rows = Mysql.queryData(stopwordsql)

    # 将查询出来的元组转换为字符串和集合
    f = lambda tup: tup[0] if tup else ""
    maprows = map(f, rows)
    content = "\n".join(maprows)
    filterwords = set(content.split('\n'))
    # 将停用词写到 stop_words.txt 文件里
    writeToFile(r"multiconfig/crawler/stop_words.txt", content, pattern='w+')

    # 查询关键词到Tag的映射
    keywords_map_tag_sql = "select `name`,directionName from ResearchDirection,Tags " \
                           "where rdid = directionId"

    keyword2tagtuple = Mysql.queryData(keywords_map_tag_sql)
    keyword2tagmap = {}
    for tup in keyword2tagtuple:
        keyword2tagmap[tup[0]] = tup[1]

    # 创建进程池
    processpool = Pool(processes=4)
    # for i in range(0, 1):
    for i in range(0, len(websiteDomains)):
        domain = websiteDomains[i]
        confDictionary1 = websiteConfInfos[i][0]
        confDictionary2 = websiteConfInfos[i][1]
        keywordConfFile = txtConfigFileNames[i]
        params = readKeywordCongig(keywordConfFile)
        for j in range(0, len(itemdics[i])):
            processName = 'process{}'.format(j)
            # print("j = {}".format(j))
            processpool.apply_async(parseSubPage,
                                    (confDictionary2, itemdics[i][j], domain, processName,
                                     params[0], params[1], keyword2tagmap, filterwords),
                                    callback=put)
    processpool.close()
    processpool.join()
    alllist = set()
    currentset = set()  # 需要插入的信息对象集合
    presistenceset = set()  # 需要更新的信息对象集合
    b = str(Mysql.queryData("select website from " + cs.db_table))  # 根据网址决定是要插入还是更新
    while not itemqueue.empty():
        #  从队列中取出解析后会议信息字典
        dic = itemqueue.get()
        website = dic.get("website")
        dic['taskname'] = conf.taskname
        #  将字典转换为Conference 对象
        c = Converter.convert_dict_to_entry(dic)
        alllist.add(c)
        if website not in b:
            #  将Conference 对象添加到当前集合里
            currentset.add(c)
        else:
            presistenceset.add(c)
    updateConferenceSet(presistenceset)
    saveConferenceSet(currentset)  # 把新爬取的会议信息保存到Mysql
    return alllist


