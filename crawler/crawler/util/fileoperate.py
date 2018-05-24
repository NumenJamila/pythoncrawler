import configparser
import json
import os
import sys


def removeFile(fileName):
    if os.path.exists(fileName):
        if os.path.isfile(fileName):
            os.remove(fileName)
            return True
        else:
            print("{f}是一个目录，不允许删除！".format(f=fileName))
            return False
    else:
        print("不存在文件：{f}".format(f=fileName))
        return False


def getFileNames(directory):
    """
    获取指定目录下的所有文件名
    :param directory: 路径
    :return: 该目录下的所有文件名或者None
    """
    if os.path.isdir(directory):
        filenames = []
        for file in os.listdir(directory):
            filename = directory + '/' + file
            if os.path.isfile(filename):
                filenames.append(filename)
        return filenames
    else:
        return None


def writeToFile(fileName, content, encoding='utf-8', pattern='a'):
    with open(fileName, pattern, encoding=encoding)as f:
        f.write(content)


def writeLinesToFile(fileName, contentList, encoding='utf-8', pattern="w"):
    """
    将str一行一行写入到文件
    :param fileName: 要写入的文件名
    :param contentList: 待写入的str列表，str要求最后以'\n'结尾
    :param encoding: 写入文件时采用的编码
    """
    with open(fileName, pattern, encoding=encoding)as f:
        f.writelines(contentList)


def readLines(fileName, encoding='utf-8'):
    """
    读取文件里每一行内容保存到列表里
    :param fileName: 读取的文件名
    :param encoding: 读取时用的编码
    :return: 每行组成的字符串列表
    """
    if os.path.exists(fileName):
        with open(fileName, encoding=encoding) as f:
            texts = f.readlines()
        text = []
        for t in texts:
            if t.strip() != '' and t != '\n':
                text.append(t.lstrip())
        return text
    else:
        return None


def formatReadContent(fileName, encoding='utf-8'):
    """
    读取指定文件并删除文件内容中的空行，同时用删除空行后的内容覆盖原文件
    :param fileName: 文件名
    :param encoding: 读取和写入文件的编码
    :return: 没有空行的内容
    """
    writeLinesToFile(fileName, readLines(fileName, encoding), encoding)
    return readContent(fileName, encoding)


def formatReadlines(fileName, encoding='utf-8'):
    writeLinesToFile(fileName, readLines(fileName, encoding), encoding)
    return readLines(fileName, encoding)


def readContent(fileName, encoding='utf-8'):
    if os.path.exists(fileName):
        with open(fileName, encoding=encoding) as f:
            texts = f.read()
        return texts
    else:
        return None


def readConfig(filename):
    """
    读取配置文件，配置文件以"xxx = xxx"的形式组织
    :param filename: 配置文件路径
    :return: 字典形式的配置文件内容
    """
    cf = configparser.ConfigParser()
    try:
        configcontent = []
        cf.read(filename, encoding="utf-8")
        sections = cf.sections()
        for s in sections:
            # configcontent.append(cf.items(s))
            dictionary = {}
            entrys = cf.items(s)
            for entry in entrys:
                dictionary[entry[0]] = entry[1]
            configcontent.append(dictionary)
    except:
        print("throw a exception:\n{e}".format(e=sys.exc_info()))
        return None
    else:
        return configcontent


def readSectionsInConfig(filename: str) -> list:
    cf = configparser.ConfigParser()
    flag = True
    try:
        cf.read(filename, encoding="utf-8")
        sections = cf.sections()
    except:
        print("throw a exception:\n{e}".format(e=sys.exc_info()))
        flag = False
    else:
        if flag:
            return sections
        else:
            return None


def writeToJson(dictionary, filename, pattern="a"):
    with open(filename, pattern, encoding='utf-8') as f:
        f.write(json.dumps(dictionary, ensure_ascii=False))


def readDictionary(filename: str) -> []:
    with open(filename, encoding='utf-8')as f:
        content = f.read()
        return json.loads(content)


def clearContent(filename: str):
    if not os.path.exists(filename):
        print("不存在 {} 文件".format(filename))
        return
    with open(filename, mode='r+', encoding='utf-8')as f:
        f.truncate()
