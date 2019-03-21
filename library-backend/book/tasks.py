from __future__ import absolute_import, unicode_literals
from SmartLibrary.celery import app
import time
import os
import sys
import django
import logging
import json
import requests
from bs4 import BeautifulSoup
import re

pathname = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(pathname)
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
sys.path.insert(0, os.path.join(BASE_DIR, 'lib'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartLibrary.settings")
django.setup()

logger = logging.getLogger(__name__)
from book.models import NewBook, RecommendBook


@app.task
def add(x, y):
    print("%d + %d = %d" % (x, y, x + y))
    return x + y


@app.task
def get_new_book_detail():
    newbook_urls = get_newbook_url()
    for url in newbook_urls:
        try:
            NewBook.objects.get(book_url=url)
        except NewBook.DoesNotExist:
            try:
                detail = get_book_detail(url)
                NewBook.objects.update_or_create(
                    title=detail['title'], subtitle=detail['subtitle'],
                    author=detail['author'], pub_date=detail['pub_date'],
                    pages=detail['pages'], book_price=detail['book_price'],
                    book_img=detail['book_img'], publisher=detail['publisher'],
                    isbn=detail['isbn'], zt_num=detail['zt_num'],
                    book_intro=detail['book_intro'], author_intro=detail['author_intro'],
                    book_catalog=detail['book_catalog'], book_url=detail['book_url'],
                    douban_res_msg=detail['douban_res_msg'], label="入门 好看",
                    db_score=8.4, emotion_1=13, emotion_2=45, emotion_3=27, emotion_4=15, emotion_5=5
                )
            except Exception as e:
                print(str(e))


@app.task
def get_recommend_book():
    recommend_urls = get_recommend_url()
    print(urls)
    for url in recommend_urls:
        try:
            RecommendBook.objects.get(book_url=url)
        except RecommendBook.DoesNotExist:
            try:
                detail = get_book_detail(url)
                RecommendBook.objects.update_or_create(
                    title=detail['title'], subtitle=detail['subtitle'],
                    author=detail['author'], pub_date=detail['pub_date'],
                    pages=detail['pages'], book_price=detail['book_price'], book_img=detail['book_img'],
                    publisher=detail['publisher'], isbn=detail['isbn'],
                    zt_num=detail['zt_num'], book_intro=detail['book_intro'],
                    author_intro=detail['author_intro'], book_catalog=detail['book_catalog'],
                    book_url=detail['book_url'], douban_res_msg=detail['douban_res_msg'],
                    label="入门 好看", db_score=8.4, emotion_1=13, emotion_2=45, emotion_3=27, emotion_4=15, emotion_5=5
                )
            except Exception as e:
                print(str(e))


def get_recommend_url():
    """
    获取推荐书籍(TOP100)的URL
    :return:
                entry_urls
    """
    entry_urls = []
    res = requests.get('http://58.194.172.34/top/top_lend.php')
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    contents = soup.select('a[class="blue"]')
    for content in contents:
        url = content['href'].replace('..', 'http://58.194.172.34')
        entry_urls.append(url)
    return entry_urls


def get_newbook_url():
    """
    获取学校图书馆新书的url
    获取的是15天之内上线的URL
    url:
            http://58.194.172.34/opac/item.php?marc_no= xxx
    page:
            range(1, 120)
    :return:list:
    ntry_url
    """
    index_url = 'http://58.194.172.34/newbook/newbook_cls_book.php?back_days={}&s_doctype={}&loca_code={}&cls={}&clsname={}&page={}'
    # 新书发布时间
    back_days = '15'
    # 文献类型 中文 西文
    s_doctype = 'ALL'
    # 校区
    loca_code = 'ALL'
    # 左侧目录编号
    cls = 'ALL'
    # 左侧目录名字
    cls_name = '全部新书'

    entry_urls = []

    for page in range(1, 120):
        res = requests.get(index_url.format(back_days, s_doctype, loca_code, cls, cls_name, page))
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        content = soup.select('.list_books')
        url_num = len(content)
        for i, item in enumerate(content):
            url = item.select('a')[0]['href'].replace('..', 'http://58.194.172.34')
            if page == 1:
                entry_urls.append(url)
            elif url in entry_urls[-url_num]:
                break
            else:
                entry_urls.append(url)
        print('finish page {}'.format(page))

    return entry_urls


def get_book_detail(book_url):
    """
    先获取ISBN 请求豆瓣 获取JSON 若JSON为空或不全 爬取学校图书馆上面的内容
    :param book_url: http://58.194.172.34/opac/item.php?marc_no= xxx
    :return:
                detail
    """
    default_book_img = 'https://img1.doubanio.com/f/shire/5522dd1f5b742d1e1394a17f44d590646b63871d/pics/book-default-lpic.gif'

    temp_detail = dict(
        title='', subtitle='', author='', pub_date='', pages='', book_price='', book_img='',
        publisher='', isbn='', zt_num='', book_intro='', author_intro='', book_catalog='',
        book_url=book_url, douban_res_msg=''
    )

    res = requests.get(book_url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = soup.select('.booklist')

    def select_dt(dt_content):
        dt_content = dt_content.select('dt')[0].text
        return dt_content

    def select_dd(dd_content):
        dd_content = dd_content.select('dd')[0].text
        return dd_content

    for item in content:
        if 'ISBN' in select_dt(item):
            temp_detail['isbn'] = int(re.sub('\D', '', str(select_dd(item).split('/')[0].replace('-', ''))))
        elif '题名/责任者' in select_dt(item):
            temp_detail['title'] = select_dd(item).split('/')[0]
            try:
                temp_detail['author'] = select_dd(item).split('/')[1]
            except IndexError:
                temp_detail['author'] = ''
        elif '出版发行项' in select_dt(item):
            temp_detail['publisher'] = select_dd(item)
        elif '载体形态项' in select_dt(item):
            temp_detail['pages'] = select_dd(item)
        elif '中图法分类号' in select_dt(item):
            temp_detail['zt_num'] = select_dd(item)
        elif '提要文摘附注' in select_dt(item):
            temp_detail['book_intro'] = select_dd(item)

    print(temp_detail['isbn'])
    if temp_detail['isbn']:
        result, detail = douban_detail(int(re.sub('\D', '', str(temp_detail['isbn']))))
        if not result:
            temp_detail['douban_res_msg'] = detail['douban_res_msg']
            temp_detail['book_img'] = default_book_img
            detail = temp_detail
            print(detail)
            return detail
        else:
            if not detail['book_img']:
                detail['book_img'] = default_book_img
            detail['book_url'] = book_url
            detail['zt_num'] = temp_detail['zt_num']
            detail['isbn'] = temp_detail['isbn']
            return detail


def douban_detail(isbn):
    """
    请求限制 注意请求过于频繁
    访问过于频繁时有可能导致内容丢失
    :param  isbn: 书本的ISBN码
    :return:
    """
    detail = {}
    time.sleep(4)
    book_url = 'https://api.douban.com/v2/book/isbn/:{}'.format(isbn)
    response = requests.get(book_url)
    response = json.loads(response.content.decode('utf-8'))
    try:
        if response['msg'] == 'book_not_found':
            detail['douban_res_msg'] = 'book_not_found'
            result = False
            return result, detail
    except KeyError:
        pass
    try:
        detail['author'] = response['author']
    except IndexError:
        detail['douban_res_msg'] = book_url
        # 只有ISBN, 没其他信息
        result = False
        return result, detail
    except KeyError:
        detail['douban_res_msg'] = book_url
        result = False
        return result, detail
    else:
        detail = {
            'author_intro': response['author_intro'], 'book_intro': response['summary'],
            'book_price': response['price'], 'author': ''.join(response['author']),
            'publisher': response['publisher'], 'isbn': response['isbn13'], 'title': response['title'],
            'pages': response['pages'], 'book_img': response['images']['small'], 'subtitle': response['subtitle'],
            'pub_date': response['pubdate'], 'book_catalog': response['catalog'], 'subject': response['id'],
            'douban_res_msg': ''
        }
        result = True

        return result, detail


if __name__ == '__main__':
    urls = get_newbook_url()
    for url in urls:
        book_detail = get_book_detail(url)
        print(book_detail)
