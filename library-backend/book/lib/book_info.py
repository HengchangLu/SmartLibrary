import json
import re
import time
import requests
from bs4 import BeautifulSoup
from lib.base_user.base_user import BaseUser
from lib.solve_captchas_with_OCR import get_verify_via_ocr


class BookInfo(object):
    """
    获取图书详细信息部分
    """
    def __init__(self):
        pass

    # @staticmethod
    # def get_newbook_url():
    #     """
    #     获取每本新书的url
    #     url:
    #             http://58.194.172.34/opac/item.php?marc_no= xxx
    #     page:
    #             range(1, 120)
    #     :return:list:
    #     ntry_url
    #     """
    #     index_url = 'http://58.194.172.34/newbook/newbook_cls_book.php?back_days={}&s_doctype={}&loca_code={}&cls={}&clsname={}&page={}'
    #     # 新书发布时间
    #     back_days = '15'
    #     # 文献类型 中文 西文
    #     s_doctype = 'ALL'
    #     # 校区
    #     loca_code = 'ALL'
    #     # 左侧目录编号
    #     cls = 'ALL'
    #     # 左侧目录名字
    #     cls_name = '全部新书'
    #
    #     entry_urls = []
    #
    #     for page in range(1, 5):
    #         res = requests.get(index_url.format(back_days, s_doctype, loca_code, cls, cls_name, page))
    #         res.encoding = 'utf-8'
    #         soup = BeautifulSoup(res.text, 'html.parser')
    #         content = soup.select('.list_books')
    #         url_num = len(content)
    #         for i, item in enumerate(content):
    #             url = item.select('a')[0]['href'].replace('..', 'http://58.194.172.34')
    #             if page == 1:
    #                 entry_urls.append(url)
    #             elif url in entry_urls[-url_num]:
    #                 break
    #             else:
    #                 entry_urls.append(url)
    #         print('Getting new book has finished page {}'.format(page))
    #
    #     return entry_urls
    #
    # @staticmethod
    # def get_recommend_url():
    #     entry_urls = []
    #     res = requests.get('http://58.194.172.34/top/top_lend.php')
    #     res.encoding = 'utf-8'
    #     soup = BeautifulSoup(res.text, 'html.parser')
    #     contents = soup.select('a[class="blue"]')
    #     for content in contents:
    #         url = content['href'].replace('..', 'http://58.194.172.34')
    #         entry_urls.append(url)
    #
    # def get_book_detail(self, book_url):
    #     """
    #     先获取ISBN 请求豆瓣 获取JSON 若JSON为空或不全 爬取学校图书馆上面的内容
    #     :param book_url: http://58.194.172.34/opac/item.php?marc_no= xxx
    #     :return:
    #                 detail
    #     """
    #
    #     default_book_img = 'https://img1.doubanio.com/f/shire/5522dd1f5b742d1e1394a17f44d590646b63871d/pics/book-default-lpic.gif'
    #
    #     global detail
    #     temp_detail = dict(
    #         title='', subtitle='', author='', pub_date='', pages='', book_price='', book_img='',
    #         publisher='', isbn='', zt_num='', book_intro='', author_intro='', book_catalog='',
    #         book_url='', douban_res_msg=''
    #     )
    #     # detail = dict(
    #     #     title='', subtitle='', author='', pub_date='', pages='', book_price='', book_img='',
    #     #     publisher='', isbn='', zt_num='', book_intro='', author_intro='', book_catalog='',
    #     #     book_url='', douban_res_msg=''
    #     # )
    #     res = requests.get(book_url)
    #     res.encoding = 'utf-8'
    #     soup = BeautifulSoup(res.text, 'html.parser')
    #     content = soup.select('.booklist')
    #
    #     for item in content:
    #         if 'ISBN' in self.select_dt(item):
    #             temp_detail['isbn'] = self.select_dd(item).split('/')[0].replace('-', '')
    #         elif '题名/责任者' in self.select_dt(item):
    #             temp_detail['title'] = self.select_dd(item).split('/')[0]
    #             try:
    #                 temp_detail['author'] = self.select_dd(item).split('/')[1]
    #             except IndexError:
    #                 temp_detail['author'] = ''
    #         elif '出版发行项' in self.select_dt(item):
    #             temp_detail['publisher'] = self.select_dd(item)
    #         elif '载体形态项' in self.select_dt(item):
    #             temp_detail['pages'] = self.select_dd(item)
    #         elif '中图法分类号' in self.select_dt(item):
    #             temp_detail['zt_num'] = self.select_dd(item)
    #         elif '提要文摘附注' in self.select_dt(item):
    #             temp_detail['book_intro'] = self.select_dd(item)
    #
    #     print(temp_detail['isbn'])
    #     if temp_detail['isbn']:
    #         result, detail = self.douban_detail(int(re.sub('\D', '', str(temp_detail['isbn']))))
    #         if not result:
    #             temp_detail['douban_res_msg'] = detail['douban_res_msg']
    #             temp_detail['book_img'] = default_book_img
    #             detail = temp_detail
    #             print(detail)
    #
    #         else:
    #             if not detail['book_img']:
    #                 detail['book_img'] = default_book_img
    #             detail['book_url'] = book_url
    #             detail['zt_num'] = temp_detail['zt_num']
    #             detail['isbn'] = temp_detail['isbn']
    #     return detail
    #
    # @staticmethod
    # def select_dt(dt_content):
    #     dt_content = dt_content.select('dt')[0].text
    #     return dt_content
    #
    # @staticmethod
    # def select_dd(dd_content):
    #     dd_content = dd_content.select('dd')[0].text
    #     return dd_content
    #
    # @staticmethod
    # def douban_detail(isbn):
    #     """
    #     请求限制 注意请求过于频繁
    #     访问过于频繁时有可能导致内容丢失
    #     :param  isbn: 书本的ISBN码
    #     :return:
    #     """
    #     detail = {}
    #     time.sleep(3)
    #     book_url = 'https://api.douban.com/v2/book/isbn/:{}'.format(isbn)
    #     response = requests.get(book_url)
    #     response = json.loads(response.content.decode('utf-8'))
    #     try:
    #         if response['msg'] == 'book_not_found':
    #             detail['douban_res_msg'] = 'book_not_found'
    #             result = False
    #             return result, detail
    #     except KeyError:
    #         pass
    #     try:
    #         detail['author'] = response['author']
    #     except IndexError:
    #         detail['douban_res_msg'] = book_url
    #         # 只有ISBN, 没其他信息
    #         result = False
    #         return result, detail
    #     except KeyError:
    #         detail['douban_res_msg'] = book_url
    #         result = False
    #         return result, detail
    #     else:
    #         detail = {
    #             'author_intro': response['author_intro'], 'book_intro': response['summary'],
    #             'book_price': response['price'], 'author': response['author'],
    #             'publisher': response['publisher'], 'isbn': response['isbn13'], 'title': response['title'],
    #             'pages': response['pages'],
    #             'book_img': response['images']['small'], 'subtitle': response['subtitle'],
    #             'pub_date': response['pubdate'],
    #             'book_catalog': response['catalog'], 'subject': response['id'], 'douban_res_msg': ''
    #         }
    #         result = True
    #
    #     return result, detail


class BookBorrowed(object):
    """
        图书借阅部分
    """
    # 续借验证码
    renew_verify_url = "http://58.194.172.34/reader/captcha.php"
    # 续借提交host
    renew_host = 'http://58.194.172.34/reader/ajax_renew.php'

    def __init__(self, account, password):
        self.account = account
        self.password = password

    def get_borrowed_book(self):
        user = BaseUser(account=self.account, password=self.password)
        session = user.login_mylib()
        my_borrow_response = session.get('http://58.194.172.34/reader/book_lst.php')
        my_borrow_response.encoding = 'utf-8'
        my_borrow_response_soup = BeautifulSoup(my_borrow_response.text, 'html.parser')
        temp_borrow_book_list = [item.text for i, item in enumerate(my_borrow_response_soup.select('.whitetext'))
                                 if i % 8 != 4 and i % 8 != 6 and i % 8 != 7]
        if len(temp_borrow_book_list):
            btn_label = my_borrow_response_soup.find_all('input', attrs={'class': 'btn'})
            check_list = []
            for i in range(len(btn_label)):
                check_list.append((btn_label[i].attrs['onclick'])[23:31])
            temp_list = []
            borrow_book_list = []
            for i, item in enumerate(temp_borrow_book_list):
                temp_list.append(item)
                if i % 5 == 4:
                    temp_list.append(check_list[int(i / 5)])
                    borrow_book_list.append(temp_list)
                    temp_list = []
            return {
                'result': True,
                'check_list': check_list,
                'borrow_book_list': borrow_book_list,
                'msg': '获取借阅记录成功',
            }
        else:
            return {
                'result': False,
                'msg': '没有任何借阅记录',
            }

    def renew_book(self, bar_code, check):
        user = BaseUser(account=self.account, password=self.password)
        session = user.login_mylib()
        session.get('http://58.194.172.34/reader/book_lst.php')
        verify_img = session.get(self.renew_verify_url)
        f = open('/usr/SmartLibrary/book/static/check.png', 'wb')
        f.write(verify_img.content)
        f.close()
        verify = get_verify_via_ocr('/usr/SmartLibrary/book/static/check.png')
        renew_response = session.get(
            self.renew_host + '?bar_code={}&check={}&captcha={}&time={}'.format(bar_code, check, verify, int(round(time.time() * 1000)))
            )
        try:
            renew_msg = re.findall(r'<font.*>(.*?)</font>', str(renew_response.text))[0]
        except IndexError:
            response = {
                'result': False,
                'renew_msg': '请求出错，请重试'
                }
        else:
            response = {
                'result': True,
                'renew_msg': str(renew_msg),
                }
        return response
