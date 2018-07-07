from django.shortcuts import render
from django.http import HttpResponse
from .models import ConferenceInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    queryset = request.GET.get('tag')
    if queryset:
        articles = ConferenceInfo.objects.filter(tag=queryset)
    else:
        articles = ConferenceInfo.objects.all()

    paginator = Paginator(articles, 2)

    page = request.GET.get('page')  # 获取页码
    try:
        articles = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        articles = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        articles = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'check/index.html', {'articles': articles})


def article_page(request, article_id):
    article = ConferenceInfo.objects.get(pk=article_id)
    return render(request, 'check/article_page.html', {'article':article})


def edit_page(request, article_id):
    if str(article_id) == '0':
        return render(request, 'check/edit_page.html')
    article = ConferenceInfo.objects.get(pk=article_id)
    return render(request, 'check/edit_page.html', {'article': article})

def edit_action(request):
    title = request.POST.get('title', 'TITLE')
    content = request.POST.get('content', 'CONTENT')
    article_id = request.POST.get('article_id','0')
    if article_id == '0':
        ConferenceInfo.objects.create(title=title,content=content)
        articles = ConferenceInfo.objects.all()
        return render(request, 'check/index.html',{'articles':articles})
    article = ConferenceInfo.objects.get(pk=article_id)
    article.title = title
    article.content = content
    article.save()
    return render(request, 'check/article_page.html', {'article': article})


def del_page(request, article_id):
    if str(article_id) == '0':
        return render(request, 'check/edit_page.html')
    article = ConferenceInfo.objects.get(pk=article_id)
    article.delete()
    articles = ConferenceInfo.objects.all()
    return render(request, 'check/index.html', {'articles': articles})