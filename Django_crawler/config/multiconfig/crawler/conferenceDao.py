from .formathelper import Conference
from .mysqlhelper import Mysql
from . import configsetting as cs


def insertConference(entry: Conference):
    Mysql.saveObject(entry, cs.db_table, set(cs.fields))


def updateConference(entry: Conference):
    Mysql.mysql_update(entry, cs.db_table, set(cs.fields))


def saveConferenceSet(conferences: set):
    for element in conferences:
        insertConference(element)


def updateConferenceSet(conferences: set):
    for element in conferences:
        updateConference(element)
