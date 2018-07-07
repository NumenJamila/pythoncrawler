import logging
import os


def getLogger(filename: str, loggername: str, level=logging.DEBUG, mode="w+"):
    if not os.path.exists(filename):
        print("未找到日志配置文件 {}".format(filename))
    logformat = '%(asctime)s %(lineno)d %(filename)-12s %(levelname)-8s \n\t%(message)s\n'
    datefmt = '%m-%d %H:%M'
    logging.basicConfig(level=level, format=logformat,
                        datefmt=datefmt, filename=filename, filemode=mode)
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(loggername)
    return logger
