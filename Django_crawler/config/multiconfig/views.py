from django.shortcuts import render
from django.http import HttpResponse
from .models import Multiconf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .crawler.main import inputDB
from .crawler.main import checkresult
from .crawler.conferenceDao import saveConferenceSet, updateConferenceSet
from .crawler.mysqlhelper import Mysql
from .crawler.typeconverter import Converter
from .crawler import configsetting as cs
import json


def index(request):
    confs = Multiconf.objects.all()

    paginator = Paginator(confs, 8)
    page = request.GET.get('page')  # 获取页码
    try:
        confs = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        confs = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        confs = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'Multiconfig/index.html',{'confs': confs})


def setconfig_page(request,conf_id):
    conf = Multiconf.objects.get(pk=conf_id)
    return render(request,'Multiconfig/setconfig_page.html',{'conf':conf})


def edit_page(request,conf_id):
    if str(conf_id) == '0':
        return render(request,'Multiconfig/edit_page.html')
    conf = Multiconf.objects.get(pk=conf_id)
    return render(request,'Multiconfig/edit_page.html',{'conf':conf})


def edit_action(request):
    taskname = request.POST.get('taskname','null')
    confConfigFileNames = request.POST.get('confConfigFileNames','null')
    txtConfigFileNames = request.POST.get('txtConfigFileNames','null')
    conf_id = request.POST.get('conf_id','0')
    if conf_id == '0':
        Multiconf.objects.create(taskname=taskname, confConfigFileNames=confConfigFileNames,
        					  txtConfigFileNames=txtConfigFileNames)
        confs = Multiconf.objects.all()
        return render(request, 'Multiconfig/index.html',{'confs':confs})
    conf = Multiconf.objects.get(pk=conf_id)
    conf.taskname = taskname
    conf.confConfigFileNames = confConfigFileNames
    conf.txtConfigFileNames = txtConfigFileNames
    conf.save()
    return render(request, 'Multiconfig/setconfig_page.html', {'conf': conf})

def del_page(request,conf_id):
    if str(conf_id) == '0':
        return render(request,'Multiconfig/edit_page.html')
    conf = Multiconf.objects.get(pk=conf_id)
    conf.delete()
    confs = Multiconf.objects.all()
    return render(request, 'Multiconfig/index.html', {'confs': confs})


def createconf(request):
    taskname = request.POST.get('taskname','taskname')
    confConfigFileNames = request.POST.get('confConfigFileNames','confConfigFileNames')
    txtConfigFileNames = request.POST.get('txtConfigFileNames','txtConfigFileNames')
    conf_id = request.POST.get('conf_id','0')
    if conf_id == '0':
        Multiconf.objects.create(taskname=taskname, confConfigFileNames=confConfigFileNames,
        					  txtConfigFileNames=txtConfigFileNames)
        confs = Multiconf.objects.all()
        return render(request, 'Multiconfig/index.html',{'confs':confs})

def check(request, conf_id):
    conf = Multiconf.objects.get(pk=conf_id)
    info_dicts = checkresult(conf)
    return render(request, 'multiconfig/checkresult.html', {"info_dicts": info_dicts})


def input(request, conf_id):
	conf = Multiconf.objects.get(pk=conf_id)
	info_dicts = inputDB(conf)
	return render(request, 'multiconfig/checkresult.html', {"info_dicts": info_dicts})

def search(request):
    request.encoding = 'utf-8'
    if request.GET.get('q') is not None:
        q = request.GET['q']
        confs = Multiconf.objects.filter(Q(req_url__icontains=q))
        if len(confs) > 0:     # 数据库中存在
            return render(request, 'Multiconfig/space.html', {"confs": confs})
        else:      # 数据库中不存在
            error_content = "还未收录此请求网址的配置文件！"
            return render(request, 'Multiconfig/space.html', {"error_content": error_content})
    else:
        confs = Multiconfv.objects.all()
        return render(request, 'Multiconfig/space.html', {"confs": confs})
 
def newconf(request):
    return render(request, 'Multiconfig/configfile.html')

def checkconf(request):
    request.encoding = 'utf-8'
    if request.GET.get('location') is not None:
        location = request.GET['location']
        print(location)
        with open(location, "r", encoding = "utf-8") as f:
            txt = f.read()
            print(txt)
    return render(request, 'Multiconfig/configfile.html', {"txt": txt, "location": location})

def savetxt(request):
    request.encoding = 'utf-8'
    if request.GET.get('txt') is not None:
        txt = request.GET['txt']
        location = request.GET['location']
        with open(location, "w", encoding = "utf-8") as f:
            f.write(txt)
    return render(request, 'Multiconfig/index.html')

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
#         ids = Multiconf.objects.all().values('id')
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
def newconfigfile(request):
	return render(request, 'multiconfig/edit_page.html')

