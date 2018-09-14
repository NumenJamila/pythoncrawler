from django.shortcuts import render
from django.http import HttpResponse
from .models import Conference
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def index(request):

    conferences = Conference.objects.all()

    paginator = Paginator(conferences, 8)
    page = request.GET.get('page')  # 获取页码
    try:
        conferences = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        conferences = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        conferences = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'conferenceinfo/index.html', {'conferences': conferences})


def conference_page(request, conference_id):
    conference = Conference.objects.get(pk=conference_id)
    return render(request, 'conferenceinfo/conference_page.html', {'conference':conference})


def edit_page(request, conference_id):
    if str(conference_id) == '0':
        return render(request, 'conferenceinfo/edit_page.html')
    conference = Conference.objects.get(pk=conference_id)
    return render(request, 'conferenceinfo/edit_page.html', {'conference': conference})

def newconference(request):
    return render(request, 'conferenceinfo/edit_page.html')

def edit_action(request):
    website = request.POST.get('website','WEBSITE')
    cnName = request.POST.get('cnName','CNNAME')
    enName = request.POST.get('enName','ENNAME')
    introduce = request.POST.get('introduce','INTRODUCE')
    location = request.POST.get('location','LOCATION')
    sponsor = request.POST.get('sponsor','SPONSOR')
    startdate = request.POST.get('startdate','STARTDATE')
    enddate = request.POST.get('enddate','ENDDATE')
    deadline = request.POST.get('deadline','DEADLINE')
    image= request.POST.get('image','IMAGE')
    tag = request.POST.get('tag','TAG')
    conference_id = request.POST.get('conference_id','0')
    if conference_id == '0':
        Conference.objects.create(website=website, cnName=cnName,
        					 enName=enName, introduce=introduce, 
        					 location=location, sponsor=sponsor, 
        					 startdate=startdate, enddate=enddate, 
        					 image=image, 
        					 tag=tag)
        conferences = Conference.objects.all()
        return render(request, 'conferenceinfo/index.html',{'conferences':conferences})
    conference = Conference.objects.get(pk=conference_id)
    if website != 'null' and website != 'None':
        conference.website = website
    if cnName != 'null' and cnName != 'None':
        conference.cnName = cnName
    if enName != 'null' and enName != 'None':
        conference.enName = enName
    if introduce != 'null' and introduce != 'None':
        conference.introduce = introduce
    if location != 'null' and location != 'None':
        conference.location = location
    if sponsor != 'null' and sponsor != 'None':
        conference.sponsor = sponsor
    if startdate != 'null' and startdate != 'None':
        conference.startdate = startdate
    if enddate != 'null' and enddate != 'None':
        conference.enddate = enddate
    if deadline != 'null' and deadline != 'None':
        conference.deadline = deadline
    if image != 'null' and image != 'None':
        conference.image = image
    if tag != 'null' and tag != 'None':
        conference.tag = tag
    conference.save()
    return render(request, 'conferenceinfo/conference_page.html', {'conference': conference})


def del_page(request, conference_id):
    if str(conference_id) == '0':
        return render(request, 'conferenceinfo/edit_page.html')
    conference = Conference.objects.get(pk=conference_id)
    conference.delete()
    conferences = Conference.objects.all()
    return render(request, 'conferenceinfo/index.html', {'conferences': conferences})

def configfile(request):
    return render(request, 'conferenceinfo/configfile.html')

def space_data(request):
    request.encoding = 'utf-8'
    if request.GET.get('q') is not None:
        q = request.GET['q']
        conferences = Conference.objects.filter(Q(website__icontains=q) | Q(cnName__icontains=q) | Q(enName__icontains=q))
        if len(conferences) > 0:     # 数据库中存在
            return render(request, 'conferenceinfo/space.html', {"conferences": conferences})
        else:      # 数据库中不存在
            error_content = "无搜索结果！"
            return render(request, 'conferenceinfo/space.html', {"error_content": error_content})
    else:
        conferences = Conference.objects.all()
        return render(request, 'conferenceinfo/space.html', {"conferences": conferences})


def space(request):
    return render(request, 'conferenceinfo/space.html')