import ctypes
from multiprocessing import Process

from multiprocessing import Queue

from multiprocessing import Value

import psutil

from crawler.process.worker import Saver


class GuardWorkerProcess(Process):
    def __init__(self, queue: Queue, processname: str, num: int,
                 savefilaname: str, saver: Saver, poolclose: Value):
        super().__init__()
        self.queue = queue  # 存放解析完成后的会议信息字典队列
        self.processname = processname  # 进程名
        self.num = num  # 从队列里取出的数据达到 num 时把 num 条数据保存下来
        self.savefilename = savefilaname
        self.p = saver
        self.poolclose = poolclose
        self.guardIsExit = Value(ctypes.c_bool, False)

    def run(self):
        while True:
            # 如果进程池已经关闭并且任务已经结束
            # poolclose.value的值在主进程里将会被设置成 True
            if self.poolclose.value:

                # poolclose.value的值为True将保存数据进程的flag值置为True
                # 保存数据进程进行最后的数据保存工作，执行完后退出
                self.p.flag.value = True
                break
            if not psutil.pid_exists(self.p.pid):
                newsaver = Saver(self.queue, self.processname, self.num, self.savefilename)
                self.p = newsaver
                newsaver.start()
        while not self.p.finish.value:
            pass
        print("守护进程退出，pid = {}".format(self.pid))
        self.guardIsExit.value = True
