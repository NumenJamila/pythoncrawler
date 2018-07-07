from util.formathelper import Conference
from util.mongodbhelper import MongoDBCRUD
from util.mysqlhelper import Mysql


def queryAllConferenceFromMongo() -> set:
    count = MongoDBCRUD.query_collection_count("conference")
    resultlist = MongoDBCRUD.query("conference", {},
                                   {"cnName": 1, "enName": 1, "website": 1, "_id": 0, "tag": 1, "location": 1,
                                    "sponsor": 1,
                                    "startdate": 1, "enddate": 1, "deadline": 1, "acceptance": 1}, 0, count)


def insertConference(entry: Conference):
    fields = ["cnName", "enName", "website", "tag",
              "image", "location", "sponsor", "startdate",
              "enddate", "deadline", "introduce"
              ]
    Mysql.saveObject(entry, "check_conferenceinfo", set(fields))


def updateConference(entry: Conference):
    fields = ["cnName", "enName", "website", "tag",
              "image", "location", "sponsor", "startdate",
              "enddate", "deadline", "introduce"
              ]
    Mysql.mysql_update(entry, "check_conferenceinfo", set(fields))


def saveConferenceSet(conferences: set):
    for element in conferences:
        insertConference(element)


def updateConferenceSet(conferences: set):
    for element in conferences:
        updateConference(element)
