import datetime
import sys
from multiprocessing import Queue

import pymongo as pm
from pymongo import MongoClient

from crawler.util.formathelper import Conference

class MongoDBCRUD(object):
    uri = "mongodb://root:root123@118.89.59.66:27017/test"
    connection = MongoClient(uri)
    db = connection.get_database("test")
    execresultqueue = Queue()

    @classmethod
    def insert(cls, dic: dict, collectionname: str):
        collection = cls.db.get_collection(collectionname)
        collection.insert_one(dic)
        MongoDBCRUD.execresultqueue.put("往数据库插入一条数据:\n{}\n\n".format(dic))

    @classmethod
    def query(cls, collectionname: str, condition: dict, itemfields: dict, skip=0, limit=50)->list:
        start = datetime.datetime.now()
        collection = cls.db.get_collection(collectionname)
        datas = collection.find(condition, itemfields).skip(skip).limit(limit)
        reslist = []
        for data in datas:
            reslist.append(data)
        end = datetime.datetime.now()
        print("查询花费时间：{}\t".format((end - start)))
        return reslist

    @classmethod
    def query_collection_count(cls, collectionname: str):
        collection = cls.db.get_collection(collectionname)
        count = collection.count()
        return count

    @classmethod
    def saveSet(cls, objset: set, collectionname: str):
        for obj in objset:
            try:
                dic = obj.__dict__
                cls.insert(dic, collectionname)
            except Exception as e:
                cls.execresultqueue.put("\t插入时出现异常： \n{}\n".format(e.__traceback__))
                print(e.__traceback__)

    @classmethod
    def closeConnection(cls):
        cls.connection.close()
        print("close database connection")
