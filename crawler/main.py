import ctypes
import datetime

from multiprocessing import Value

from crawler.process.guardprocess import GuardWorkerProcess
from crawler.process.worker import Saver
from crawler.spider.logmanage import loadLogger
from crawler.util.fileoperate import *
from crawler.spider.analysesources import HtmlCodeHandler
from crawler.spider.subpagehandle import readKeywordCongig, parseSubPage
from multiprocessing import Queue
from multiprocessing import Pool
import sys
import time

from crawler.util.mysqlhelper import Mysql


def put(dic: dict):
    global itemqueue
    if len(dic) > 2:
        itemqueue.put(dic)


def showDict(dic: dict):
    print("callback -----> {}".format(dic))


if __name__ == '__main__':
    # 清空日志内容
    clearContent('file/log/debug.log')
    clearContent('file/log/info.log')

    startTime = datetime.datetime.now()

    # 加载日志配置文件
    logger = loadLogger('file/log/applogconfig.ini')
    logger.info("主进程id为：\t{}".format(os.getpid()))

    # 读取爬虫配置文件
    configFileNames = getFileNames('file/config/')
    findConf = lambda name: name[name.rindex('.') + 1:].lower() == 'conf'
    findTxt = lambda name: name[name.rindex('.') + 1:].lower() == 'txt'
    # 获取file/config/目录下所有的*.conf配置文件
    confConfigFileNames = list(filter(findConf, configFileNames))
    # 获取file/config/目录下所有的*.txt配置文件
    txtConfigFileNames = list(filter(findTxt, configFileNames))
    logger.debug('\nfile/config/目录下的.conf文件有：\n{}\n'.format(confConfigFileNames))
    logger.debug('\nfile/config/目录下的.txt文件有：\n{}\n'.format(txtConfigFileNames))
    savejsonfilenames = []  # 初次抓取的目标信息保存的路径

    # 生成初次爬取信息的临时文件名
    for i in range(1, len(confConfigFileNames) + 1):
        name = 'file/log/{}.json'.format(i)
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
    logger.info("所有子进程执行完")
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
            secondcfg = dict(dicList[1])  # 读取配置文件第2节子页配置
            websiteConfInfos.append([firstcfg, secondcfg])

    itemqueue = Queue()

    resultFileName = 'file/log/result.json'
    removeFile(resultFileName)
    writeToFile(resultFileName, '[\n')

    # 创建进程池
    processpool = Pool(processes=3)

    #  创建1个用于保存解析完成后的会议信息进程, 解析的会议字典满20条保存一次
    saver = Saver(itemqueue, "saveprocess", 20, resultFileName)
    #  将 saver 进程设置为守护进程
    # saver.daemon = True
    poolclose = Value(ctypes.c_bool, False)

    guarder = GuardWorkerProcess(itemqueue, "saveprocess", 20, resultFileName, saver, poolclose)
    saver.start()
    guarder.start()
    logger.info("守护saver的进程： pid = {} is start".format(guarder.pid))

    # 查询所有停用的过滤词
    stopwordsql = "select word from JiebaStopWord"
    rows = Mysql.queryData(stopwordsql)

    # 将查询出来的元组转换为字符串和集合
    f = lambda tup: tup[0] if tup else ""
    maprows = map(f, rows)
    content = "\n".join(maprows)
    filterwords = set(content.split('\n'))
    # 将停用词写到 stop_words.txt 文件里
    writeToFile("file/txt/stop_words.txt", content, pattern='w+')

    # 查询关键词到Tag的映射
    keywords_map_tag_sql = "select `name`,directionName from ResearchDirection,Tags " \
                           "where rdid = directionId"

    keyword2tagtuple = Mysql.queryData(keywords_map_tag_sql)
    keyword2tagmap = {}
    for tup in keyword2tagtuple:
        keyword2tagmap[tup[0]] = tup[1]

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

    # 设置共享内存变量 poolclose 的值，让守护进程通知爬取信息的进程池任务已经结束
    # 守护进程可以不必守护保存数据进程，并通知保存数据的进程做最后的数据保存工作
    poolclose.value = True
    print("\n\t抓取数据的进程任务结束\n")
    logger.info("\t\t抓取数据的进程任务结束\n")

    while not guarder.guardIsExit.value:
        time.sleep(2)
        print("守护进程:guarder.guardIsExit  = {}, pid = {}"
              .format(guarder.guardIsExit.value, guarder.pid))

    writeToFile(resultFileName, '\n{}\n]')

    finishTime = datetime.datetime.now()
    logger.info("程序总共运行时间为 {}".format(finishTime - startTime))
    print("\nDone!\n")
    logger.debug("\nDone!\n")
