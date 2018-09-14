from django.shortcuts import render
from django.http import HttpResponse
from .models import Config
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .crawler.urllibhelper import SpiderApi
from pyquery import PyQuery as pq
import re
from .crawler.conferenceDao import saveConferenceSet, updateConferenceSet
from .crawler.mysqlhelper import Mysql
from .crawler.typeconverter import Converter
from .crawler import configsetting as cs
from .crawler.taghanldler import extractTagFiles
from .crawler.fileoperate import *
from django.db.models import Q

def index(request):
    confs = Config.objects.all()

    paginator = Paginator(confs, 8)
    page = request.GET.get('page')  # 获取页码
    try:
        confs = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        confs = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        confs = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'setconfig/index.html',{'confs': confs})


def setconfig_page(request,conf_id):
    conf = Config.objects.get(pk=conf_id)
    return render(request,'setconfig/setconfig_page.html',{'conf':conf})


def edit_page(request,conf_id):
    if str(conf_id) == '0':
        return render(request,'setconfig/edit_page.html')
    conf = Config.objects.get(pk=conf_id)
    return render(request,'setconfig/edit_page.html',{'conf':conf})


def edit_action(request):
    taskname = request.POST.get('taskname','null')
    website_select = request.POST.get('website_select','null')
    website_reg = request.POST.get('website_reg','null')
    cnName_select = request.POST.get('cnName_select','null')
    cnName_reg = request.POST.get('cnName_reg','null')
    enName_select = request.POST.get('enName_select','null')
    enName_reg = request.POST.get('enName_reg','null')
    introduce_select = request.POST.get('introduce_select','null')
    introduce_reg = request.POST.get('introduce_reg','null')
    location_select = request.POST.get('location_select','null')
    location_reg = request.POST.get('location_reg','null')
    sponsor_select = request.POST.get('sponsor_select','null')
    sponsor_reg = request.POST.get('sponsor_reg','null')
    startdate_select = request.POST.get('startdate_select','null')
    startdate_reg = request.POST.get('startdate_reg','null')
    enddate_select = request.POST.get('enddate_select','null')
    enddate_reg = request.POST.get('enddate_reg','null')
    deadline_select = request.POST.get('deadline_select','null')
    deadline_reg = request.POST.get('deadline_reg','null')
    image_select = request.POST.get('image_select','null')
    image_reg = request.POST.get('image_reg','null')
    tag_select = request.POST.get('tag_select','null')
    tag_reg = request.POST.get('tag_reg','null')
    req_url = request.POST.get('req_url','null')
    conf_id = request.POST.get('conf_id','0')
    if conf_id == '0':
        Config.objects.create(website_select=website_select, website_reg=website_reg,
        					  cnName_select=cnName_select, cnName_reg=cnName_reg,
        					 enName_select=enName_select, enName_reg=enName_reg, 
        					 introduce_select=introduce_select, introduce_reg=introduce_reg, 
        					 location_select=location_select,location_reg=location_reg, 
        					 sponsor_select=sponsor_select, sponsor_reg=sponsor_reg, 
        					 startdate_select=startdate_select, startdate_reg=startdate_reg,
        					 enddate_select=enddate_select, enddate_reg=enddate_reg, 
        					 deadline_select=deadline_select, deadline_reg=deadline_reg,
        					 image_select=image_select, image_reg=image_reg, 
        					 tag_select=tag_select, tag_reg=tag_reg, req_url=req_url,
                             taskname=taskname)
        confs = Config.objects.all()
        return render(request, 'setconfig/index.html',{'confs':confs})
    conf = Config.objects.get(pk=conf_id)
    conf.taskname = taskname
    conf.website_select = website_select
    conf.website_reg = website_reg
    conf.cnName_select = cnName_select
    conf.cnName_reg = cnName_reg
    conf.enName_select = enName_select
    conf.enName_reg = enName_reg
    conf.introduce_select = introduce_select
    conf.introduce_reg = introduce_reg
    conf.location_select = location_select
    conf.location_reg = location_reg
    conf.sponsor_select = sponsor_select
    conf.sponsor_reg = sponsor_reg
    conf.startdate_select = startdate_select
    conf.startdate_reg = startdate_reg
    conf.enddate_select = enddate_select
    conf.enddate_reg = enddate_reg
    conf.deadline_select = deadline_select
    conf.deadline_reg = deadline_reg
    conf.image_select = image_select
    conf.image_reg = image_reg
    conf.tag_select = tag_select
    conf.tag_reg = tag_reg
    conf.req_url = req_url
    conf.save()
    return render(request, 'setconfig/setconfig_page.html', {'conf': conf})

def del_page(request,conf_id):
    if str(conf_id) == '0':
        return render(request,'setconfig/edit_page.html')
    conf = Config.objects.get(pk=conf_id)
    conf.delete()
    confs = Config.objects.all()
    return render(request, 'setconfig/index.html', {'confs': confs})

def newconfigfile(request):
    return render(request, 'setconfig/edit_page.html')


def mod(conf_id):
    conf = Config.objects.get(pk=conf_id)
    per_info_key = ['website', 'cnName', 'enName', 'introduce',
                    'location', 'sponsor', 'startdate', 'enddate',
                    'deadline', 'image', 'tag']
    per_info_select = [conf.website_select, conf.cnName_select, conf.enName_select,
                       conf.introduce_select, conf.location_select, conf.sponsor_select,
                       conf.startdate_select, conf.enddate_select,
                       conf.deadline_select, conf.image_select, conf.tag_select]
    per_info_reg = [conf.website_reg, conf.cnName_reg, conf.enName_reg,
                    conf.introduce_reg, conf.location_reg, conf.sponsor_reg,
                    conf.startdate_reg, conf.enddate_reg,
                    conf.deadline_reg, conf.image_reg, conf.tag_reg]
    per_info_value = []
    req_url = conf.req_url
    html = SpiderApi.getPageSourceCode(req_url)
    doc = pq(html)
    for it in range(0, len(per_info_key)):
        try:
            per_info_value.append(doc(per_info_select[it]).text())
            print(per_info_value[it])
        except:
            per_info_value.append("")
        if per_info_reg[it] != "null":
            try:
                per_info_value[it] = re.findall((per_info_reg[it]), per_info_value[it])[0]
            except Exception as e:
                print(e)
        if per_info_select[it] == "pass":
            per_info_value[it] = per_info_reg[it]
    # 获得的信息点以字典形式存储
    info_dict = {}
    for i in range(0, len(per_info_key)):
        if per_info_value[i] != "" and per_info_value[i] != "null" and per_info_value[i] != "None":
            info_dict[per_info_key[i]] = per_info_value[i]
    
    info_dict['taskname'] = conf.taskname
    # 查询所有停用的过滤词
    stopwordsql = "select word from JiebaStopWord"
    rows = Mysql.queryData(stopwordsql)

    # 将查询出来的元组转换为字符串和集合
    f = lambda tup: tup[0] if tup else ""
    maprows = map(f, rows)
    content = "\n".join(maprows)
    filterwords = set(content.split('\n'))
    # 将停用词写到 stop_words.txt 文件里
    writeToFile(r"setconfig/crawler/stop_words.txt", content, pattern='w+')

    # 查询关键词到Tag的映射
    keywords_map_tag_sql = "select `name`,directionName from ResearchDirection,Tags " \
                           "where rdid = directionId"

    keyword2tagtuple = Mysql.queryData(keywords_map_tag_sql)
    keyword2tagmap = {}
    for tup in keyword2tagtuple:
        keyword2tagmap[tup[0]] = tup[1]
    extractTagFiles(keyword2tagmap, info_dict, filterwords)
    return info_dict

def check(request, conf_id):
    info_dict = mod(conf_id)
    c = Converter.convert_dict_to_entry(info_dict)
    return render(request, 'setconfig/checkresult.html', {'info_dict':c,'conf_id':conf_id})

    
def input(request, conf_id):
    info_dict = mod(conf_id)
    currentset = set()  # 需要插入的信息对象集合
    presistenceset = set()  # 需要更新的信息对象集合
    website = info_dict.get("website")
    b = str(Mysql.queryData("select website from " + cs.db_table))  # 根据网址决定是要插入还是更新
    #  将字典转换为Conference 对象
    c = Converter.convert_dict_to_entry(info_dict)
    if website not in b:
        #  将Conference 对象添加到当前集合里
        currentset.add(c)
    else:
        presistenceset.add(c)
    updateConferenceSet(presistenceset)
    saveConferenceSet(currentset)  # 把新爬取的会议信息保存到Mysql
    return render(request, 'setconfig/inputresult.html', {'info_dict':info_dict})

def search(request):
    request.encoding = 'utf-8'
    if request.GET.get('q') is not None:
        q = request.GET['q']
        confs = Config.objects.filter(Q(req_url__icontains=q))
        if len(confs) > 0:     # 数据库中存在
            return render(request, 'setconfig/space.html', {"confs": confs})
        else:      # 数据库中不存在
            error_content = "还未收录此请求网址的配置文件！"
            return render(request, 'setconfig/space.html', {"error_content": error_content})
    else:
        confs = Configv.objects.all()
        return render(request, 'setconfig/space.html', {"confs": confs})
 
# from apscheduler.schedulers.background import BackgroundScheduler  
# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job  
# try:    
#     # 实例化调度器  
#     scheduler = BackgroundScheduler()  
#     # 调度器使用DjangoJobStore()  
#     scheduler.add_jobstore(DjangoJobStore(), "default")  
#     # 'cron'方式循环，周一到周五，每天12:23:10执行,id为工作ID作为标记  
#     # ('scheduler',"interval", seconds=1)  #用interval方式循环，每一秒执行一次  
#     @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='16', minute='01', second='00',id='task_time',misfire_grace_time=30)  
#     def test_job():  
#         ids = Config.objects.all().values('id')
#         for item in ids:
#             id = item.get('id')
#             info_dict = mod(id)
#             currentset = set()  # 需要插入的信息对象集合
#             presistenceset = set()  # 需要更新的信息对象集合
#             website = info_dict.get("website")
#             b = str(Mysql.queryData("select website from " + cs.db_table))  # 根据网址决定是要插入还是更新
#             #  将字典转换为Conference 对象
#             c = Converter.convert_dict_to_entry(info_dict)
#             if website not in b:
#                 #  将Conference 对象添加到当前集合里
#                 currentset.add(c)
#             else:
#                 presistenceset.add(c)
#             updateConferenceSet(presistenceset)
#             saveConferenceSet(currentset)  # 把新爬取的会议信息保存到Mysql
#             print("定时爬取id为{}成功".format(id))

#     # 监控任务  
#     register_events(scheduler)  
#     # 调度器开始  
#     scheduler.start()  
# except Exception as e:  
#     print(e)  
#     # 报错则调度器停止执行  
#     scheduler.shutdown()