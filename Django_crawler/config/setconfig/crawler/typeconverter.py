from datetime import datetime

from .formathelper import Conference, DateFormatHelper
# from faulthandler import  Conference, DateFormatHelper

class Converter(object):
    @staticmethod
    def convert_dict_to_entry(diccopy: dict) -> Conference:

        # 将字典中的 startdate 字符串格式化后转换为datetime对象
        dic = diccopy.copy()
        try:
            startdate = dic.get("startdate")
            if isinstance(startdate, str):
                startdate = DateFormatHelper.convertStandardDateFormat(startdate)
                tmp = startdate.split("-")
                if len(tmp) == 3:
                    startdate = datetime(int(tmp[0]), int(tmp[1]), int(tmp[2]))
                dic["startdate"] = startdate
        except:
            dic.pop("startdate")

        # 将字典中的 enddate 字符串格式化后转换为datetime对象
        try:
            enddate = dic.get("enddate")
            if isinstance(enddate, str):
                enddate = DateFormatHelper.convertStandardDateFormat(enddate)
                tmp = enddate.split("-")
                if len(tmp) == 3:
                    enddate = datetime(int(tmp[0]), int(tmp[1]), int(tmp[2]))
                dic["enddate"] = enddate
        except:
            dic.pop("enddate")

        # 将字典中的 deadline 字符串格式化后转换为datetime对象
        try:
            deadline = dic.get("deadline")
            if isinstance(deadline, str):
                deadline = DateFormatHelper.convertStandardDateFormat(deadline)
                tmp = deadline.split("-")
                if len(tmp) == 3:
                    deadline = datetime(int(tmp[0]), int(tmp[1]), int(tmp[2]))
                dic["deadline"] = deadline
        except:
            dic.pop("deadline")
        # 返回 Conference 对象
        return Conference(dic)
