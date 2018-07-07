# -*- coding: utf-8 -*-
from util.mysqlhelper import Mysql
# Mysql.deleteBySql("delete from test.ConferenceInfo")
# Mysql.updateTable("update ConferenceInfo set tag=%s where tag=%s", ("机器学习", "machine learning"))
def get_conf_online():
    a = Mysql.queryData("select * from config_article")
    field = ['req_url', 'website_select', 'website_reg', 'cnName_select',
             'cnName_reg', 'enName_select', 'enName_reg', 'introduce_select',
             'introduce_reg', 'location_select', 'location_reg', 'sponsor_select',
             'sponsor_reg', 'startdate_select', 'startdate_reg',
             'enddate_select', 'enddate_reg', 'deadline_select', 'deadline_reg',
             'image_select', 'image_reg', 'tag_select', 'tag_reg'
             ]
    for item in a:
        with open("file/configreg/website"+str(item[0])+".conf", 'w', encoding='utf-8') as f:
            f.write("[a]")
            for i in range(0, len(field)):
                f.write("\n")
                f.write(str(field[i]) + "=" + str(item[i+1]))
    print(a)
