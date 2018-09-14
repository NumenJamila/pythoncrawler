db = "conf"

db_table = "conferenceinfo_conference"  # 数据库会议表名

db_conf_table = "setconfig_config"

fields = ["cnName", "enName", "website", "tag",  # 数据库会议表的字段
          "image", "location", "sponsor", "startdate",
          "enddate", "deadline", "introduce","taskname"
         ]

field = ['req_url', 'website_select', 'website_reg', 'cnName_select',  # 数据库配置文件表的字段
         'cnName_reg', 'enName_select', 'enName_reg', 'introduce_select',
         'introduce_reg', 'location_select', 'location_reg', 'sponsor_select',
         'sponsor_reg', 'startdate_select', 'startdate_reg',
         'enddate_select', 'enddate_reg', 'deadline_select', 'deadline_reg',
         'image_select', 'image_reg', 'tag_select', 'tag_reg'
        ]