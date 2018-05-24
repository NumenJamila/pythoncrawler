import pymysql
import sys

from multiprocessing import Queue


class Mysql(object):
    __slots__ = ()
    host = "118.89.59.66"
    port = 3306
    user = "root"
    password = "admin123?"
    db = "test"
    charset = "utf8"
    mysqlexecresultqueue = Queue()

    def __init__(self):
        pass

    @staticmethod
    def addToDb(sql, params):
        """
       往数据库插入一条数据
       :param sql: sql语句
       :param params: sql语句中的参数对应的值，params为元组类型
       :return: 受影响的行
       """
        connect = pymysql.connect(host=Mysql.host, port=Mysql.port, user=Mysql.user, passwd=Mysql.password,
                                  db=Mysql.db, charset=Mysql.charset)
        cur = connect.cursor()
        affect_line = 0
        try:
            cur.execute(sql, params)
            connect.commit()
            affect_line = cur.rowcount
        except Exception as e:
            print("sql执行异常：{e}".format(e=e))
            connect.rollback()
        else:
            connect.close()
            return affect_line

    @staticmethod
    def queryData(sql, params=None):
        connect = pymysql.connect(host=Mysql.host, port=Mysql.port, user=Mysql.user, passwd=Mysql.password,
                                  db=Mysql.db, charset=Mysql.charset)
        cur = connect.cursor()
        rows = None
        try:
            if params is not None:
                cur.execute(sql, params)
            else:
                cur.execute(sql)
            connect.commit()
            rows = cur.fetchall()
        except Exception as e:
            print("sql执行出现了异常%s" % e)
            connect.rollback()
        finally:
            connect.close()
        return rows

    @staticmethod
    def updateTable(sql, params):
        connect = pymysql.connect(host=Mysql.host, port=Mysql.port, user=Mysql.user, passwd=Mysql.password,
                                  db=Mysql.db, charset=Mysql.charset)
        cur = connect.cursor()
        affect_line = 0
        try:
            cur.execute(sql, params)
            connect.commit()
            affect_line = cur.rowcount
        except:
            print("异常信息：%s" % sys.exc_info())
        finally:
            connect.close()
        return affect_line

    @staticmethod
    def deleteById():
        connect = pymysql.connect(host=Mysql.host, port=Mysql.port, user=Mysql.user, passwd=Mysql.password,
                                  db=Mysql.db, charset=Mysql.charset)
        cur = connect.cursor()
        affect_line = 0
        sql = "delete from ConferenceInfo where id = 2417"
        try:
            cur.execute(sql)
            connect.commit()
            affect_line = cur.rowcount
        except:
            print("删除失败异常信息：")
        finally:
            connect.close()
        return affect_line

    @staticmethod
    def saveObject(obj: object, table: str, fields: set):
        # 获取对象字段字典
        dic = obj
        keys = list(dic.keys())
        # 删除对象字段字典中值为None的键值对
        for k in keys:
            if dic.get(k) is None:
                dic.pop(k)
        # 获取要插入到数据库的非None字段
        keys = list(dic.keys() & fields)
        connect = pymysql.connect(host=Mysql.host, port=Mysql.port, user=Mysql.user, passwd=Mysql.password,
                                  db=Mysql.db, charset=Mysql.charset)
        cur = connect.cursor()
        affect_line = 0
        sql = "insert into {} ( ".format(table)
        for i in range(0, len(keys)):
            sql += keys[i]
            if i < len(keys) - 1:
                sql += ","
            else:
                sql += ")"
        sql += "values("
        for i in range(0, len(keys)):
            sql += "%s"
            if i < len(keys) - 1:
                sql += ","
            else:
                sql += ")"
        queue = Mysql.mysqlexecresultqueue
        try:
            queue.put("执行sql语句：\t{}".format(sql))
            print("执行sql语句：\t{}".format(sql))
            params = []
            for i in range(0, len(keys)):
                params.append(dic.get(keys[i]))
            cur.execute(sql, tuple(params))
            connect.commit()
            affect_line = cur.rowcount
        except Exception as e:
            print("mysql插入数据出现异常：{e}".format(e=e))
            queue.put("mysql执行语句： {} 时出现异常\n异常原因： {}\n".format(sql, e))
            connect.rollback()
        finally:
            connect.close()
            return affect_line

    @staticmethod
    def mysql_update(dic: object, table: str, fields: set, website: str):
        keys = list(dic.keys())
        # 删除对象字段字典中值为None的键值对
        for k in keys:
            if dic.get(k) is None:
                dic.pop(k)
        # 获取要插入到数据库的非None字段
        keys = list(dic.keys() & fields)
        connect = pymysql.connect(host=Mysql.host, port=Mysql.port, user=Mysql.user, passwd=Mysql.password,
                                  db=Mysql.db, charset=Mysql.charset)
        cur = connect.cursor()
        affect_line = 0
        sql = "update {} ".format(table)
        sql += "set "
        for i in range(0, len(keys)):
            sql += keys[i]
            if i < len(keys) - 1:
                sql += "=%s,"
            else:
                sql += "=%s "
        sql += "where website=%s"
        queue = Mysql.mysqlexecresultqueue
        try:
            queue.put("执行sql语句：\t{}".format(sql))
            print("执行sql语句：\t{}".format(sql))
            params = []
            for i in range(0, len(keys)):
                params.append(dic.get(keys[i]))
            params.append(dic.get("website"))
            print(params)
            cur.execute(sql, tuple(params))
            connect.commit()
            affect_line = cur.rowcount
        except Exception as e:
            print("mysql更新数据出现异常：{}".format(e))
            queue.put("mysql执行语句： {} 时出现异常\n异常原因： {}\n".format(sql, e))
            connect.rollback()
        finally:
            connect.close()
            return affect_line