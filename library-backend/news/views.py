import json
from django.http import HttpResponse
import requests
import re
from bs4 import BeautifulSoup
from .models import NoticeNews, SourceNews, LectureNews, ServiceSummaryNews
from django.forms import model_to_dict
from django.shortcuts import render
from .lib.news_info import NewsInfo
from lib.base.exceptions import *
from lib.base.base_lib import *


def post_file(request):
    if request.method == "GET":
        return render(request, 'postfile.html')
    if request.method == 'POST':
        file = request.FILES.get("myfile", None)
        if not file:
            return HttpResponse("no files for upload")
        news_list = []
        news_dict = {}
        with open(file.name, 'r', encoding='gbk') as f:
            title = ''
            url = ''
            flag = 0
            for line in f.read():
                if line == ' ':
                    flag = 1
                    continue
                if line == '\n':
                    flag = 0
                    news_dict[title] = url
                    title = ''
                    url = ''
                    continue
                if flag == 0:
                    title = title + line
                if flag == 1:
                    url = url + line
            news_dict[title] = url
            news_list.append(news_dict)
        news_list = [ServiceSummaryNews(title=key, url=value) for key, value in news_dict.items()]
        ServiceSummaryNews.objects.bulk_create(news_list)
        return HttpResponse('OK')


@api_response
def get_news(request):
    """
    图书馆公告消息 讲座信息 资源动态
    :param request:
                current_tab: 新闻类型
                news_page_num: 新闻的页数
                callback_count: 每次返回到前端新闻条数
    :return:
            result: True
            msg:
            news_list:
    """
    try:
        current_tab = int(request.GET['currentTab'])
        news_page_num = int(request.GET['newsPageNum'])
        callback_count = int(request.GET['callbackCount'])
        target_model = [[LectureNews, SourceNews][current_tab == 2], NoticeNews][current_tab == 1]
    except Exception as e:
        raise RequestParamError(str(e))
    else:
        try:
            target_model.objects.get(current_tab=current_tab)
        except target_model.DoesNotExist:
            update_news = NewsInfo(current_tab, page_num=50)
            update_news.update_news()
        else:
            update_news = NewsInfo(current_tab, page_num=1)
            update_news.update_news()
        finally:
            news = NewsInfo(current_tab, page_num=None)
            news_list = news.get_news_list(news_page_num, callback_count)
            response = {
                'result': True,
                'msg': '获取新闻内容成功！',
                'news_list': news_list,
            }
            return response


@api_response
def get_news_detail(request):
    """
    图书馆公告消息 讲座信息 资源动态 正文 详情
    :param request:
                    id: 新闻的id
                    current_tab: 新闻类型
    :return:
            content：内容
    """
    try:
        news_id = request.GET['id']
        current_tab = int(request.GET['currentTab'])
    except Exception as e:
        raise RequestParamError(str(e))
    else:
        news_detail = NewsInfo(current_tab=current_tab, page_num=None)
        response = news_detail.get_news_detail(news_id)
        return response


@api_response
def get_summary(request):
    """
    图书馆概况页
    :param request:
                title: 以标题为检索
    :return:
    """
    try:
        title = request.GET.get('title')
        url = request.GET.get('url')
        if url == '':
            search_article = ServiceSummaryNews.objects.get(title=title)
            url = search_article.url
    except Exception as e:
        raise RequestParamError(str(e))
    else:
        summary_service_detail = NewsInfo(current_tab=None, page_num=None)
        response = summary_service_detail.get_summary_service(url)
        return response


def service_summary(request):
    """
    服务与交流页
    :param request:
    :return:
    """
    title = request.GET.get('title')
    url = request.GET.get('url')
    if url == '':
        search_article = ServiceSummaryNews.objects.get(title=title)
        url = search_article.url
    # 获取标题 时间 正文
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.select('.article h2[align="center"]')[0].text
    time = soup.select('.article div[align="center"]')[0].text.split()[1]
    temp_content = soup.select('.article div[style="font-size:11pt;"] ')
    content = ' '.join(item for item in str(temp_content[0]).split())
    content = content.replace('font-family: 仿宋;', '').replace('FONT-FAMILY: 仿宋;', '')
    content = re.sub(r"<.?o:p>", "", content)
    content = re.sub(r"<.?xml:namespace prefix.*?>", '', content)

    response = {
        'result': True,
        'title': title,
        'time': time,
        'url': url,
        'content': content,
    }
    return HttpResponse(json.dumps(response, ensure_ascii=False))
