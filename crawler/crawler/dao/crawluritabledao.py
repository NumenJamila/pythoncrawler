import traceback

from crawler.util.mysqlhelper import Mysql


class CrawledURLDao(object):

    @classmethod
    def insertURLS(cls, urls: set):
        success = 0
        for url in urls:
            try:
                sql = "insert into CrawledURI(uri) values(%s)"
                Mysql.addToDb(sql, (url))
                success += 1
            except Exception as e:
                print("insert exception:\t {}".format(traceback.format_exc()))
        return success
