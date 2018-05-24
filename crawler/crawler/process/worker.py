import ctypes
from multiprocessing import Process

from multiprocessing import Queue

from multiprocessing import Value

from crawler.dao.conferenceDao import saveConferenceSet
from crawler.spider.logmanage import loadLogger
from crawler.util.fileoperate import writeToJson, writeToFile
from crawler.util.mongodbhelper import MongoDBCRUD
from crawler.util.mysqlhelper import Mysql
from crawler.util.typeconverter import Converter
workerlogger = loadLogger('file/log/customlog.ini')


class Saver(Process):

    def __init__(self, queue: Queue, processname: str, num: int, savefilaname: str):
        super().__init__()
        self.queue = queue  # 存放解析完成后的会议信息字典队列
        self.processname = processname  # 进程名
        self.num = num  # 从队列里取出的数据达到 num 时把 num 条数据保存下来
        self.savefilename = savefilaname
        self.flag = Value(ctypes.c_bool, False)
        self.finish = Value(ctypes.c_bool, False)

    def run(self):
        workerlogger.info("\n\tsave conference process {} is starting\n\n".format(self.pid))
        print("process pid={} start!".format(self.pid))
        currentset = set()
        while True:
            if self.flag.value:
                print("self.flag = {}".format(self.flag.value))
                workerlogger.info("self.flag = {}\n".format(self.flag.value))
                workerlogger.info("集合中还剩下 {} 条数据".format(len(currentset)))
                if len(currentset) > 0:
                    try:
                        count = MongoDBCRUD.query_collection_count("conference")
                        self.savecore(count, currentset)
                        saveConferenceSet(currentset)
                    except Exception as e:
                        workerlogger.error("发生异常：\n{}\n".format(e))
                        print("操作数据库时发生异常：\n{}\n".format(e))
                    finally:
                        execresultqueue = MongoDBCRUD.execresultqueue
                        while not execresultqueue.empty():
                            workerlogger.info(execresultqueue.get())
                self.finish.value = True
                break
            while not self.queue.empty():
                #  从队列中取出解析后会议信息字典
                dic = self.queue.get()

                #  将字典转换为Conference 对象
                c = Converter.convert_dict_to_entry(dic)

                #  将Conference 对象添加到当前集合里
                currentset.add(c)
                try:
                    writeToJson(dic, self.savefilename)
                    writeToFile(self.savefilename, ',\n')
                except Exception as e:
                    workerlogger.error("写入文件时出现异常，异常信息如下：\n{}\n".format(e))
                if len(currentset) >= self.num:
                    try:
                        count = MongoDBCRUD.query_collection_count("conference")

                        # 把新爬取的会议信息保存进MongoDB
                        self.savecore(count, currentset)

                        # 把新爬取的会议信息保存到Mysql
                        saveConferenceSet(currentset)
                        currentset.clear()
                        workerlogger.debug("\t\t清空集合后，集合个数为:{}\n".format(len(currentset)))
                    except Exception as e:
                        workerlogger.error("操作数据库时出现了异常：\n{}\n".format(e))
                        workerlogger.info("集合中还剩下 {} 条数据\n".format(len(currentset)))
                        print(e)
                    finally:
                        while not Mysql.mysqlexecresultqueue.empty():
                            workerlogger.info(Mysql.mysqlexecresultqueue.get())
        print("saver process exit!")

    def savecore(self, count, currentset):
        """
        对抓取的数据中去除与数据库重复部分
        :param count: 数据库中的总记录条数
        :param currentset: 进程解析后得到的最终目标会议对象集合
        """
        skip = 0  # skip表示每次跳过的数据条数
        crawlset = currentset
        while skip <= count:
            #  每次查询 500 条conference信息，只取 cnName、enName、website 3个字段
            recordlist = MongoDBCRUD.query("conference", {},
                                           {"cnName": 1, "enName": 1, "website": 1, "_id": 0},
                                           skip, 500)
            presistenceset = set()  # 从数据库取出的conference信息对象集合
            for record in recordlist:
                entry = Converter.convert_dict_to_entry(record)
                presistenceset.add(entry)

            workerlogger.info("当前抓取的数据数量为：{}".format(len(crawlset)))
            print("当前抓取的数据数量为：{}".format(len(crawlset)))

            crawlset = crawlset - presistenceset

            workerlogger.info("抓取的数据去重后的数量为：{}".format(len(crawlset)))
            print("抓取的数据去重后的数量为：{}\n\n".format(len(crawlset)))
            skip += 500

        # 将去重后的数据保存到数据库
        MongoDBCRUD.saveSet(crawlset, "conference")
        # 写数据库操作日志
        dbexecresqueue = MongoDBCRUD.execresultqueue
        while not dbexecresqueue.empty():
            workerlogger.debug(dbexecresqueue.get())
