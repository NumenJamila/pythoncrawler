from multiprocessing import Manager, Pool, Queue
import os,time ,random


def reader(q):
    print('reader启动%s,父进程为%s' % (os.getpid(), os.getppid()))
    for i in range(q.qsize()):
        print('reader从Queue获取消息 %s' % q.get(True))


def writer(q):
    print('writer启动%s,父进程为%s' % (os.getpid(), os.getppid()))
    for i in 'hello world':
        q.put(i)


if  __name__ == '__main__':
    q = Manager().Queue()
    pool= Pool()
    pool.apply_async(writer, (q,))


    time.sleep(1)   #让写任务先写完数据，下面再向队列写数据
    pool.apply_async(reader, (q,))
    pool.close()
    pool.join()
    print('(%s) END ' % os.getpid())