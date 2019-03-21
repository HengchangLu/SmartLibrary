import re
import requests
from bs4 import BeautifulSoup
import json
import time

# isbn = '9787020027606'
douban_url = 'http://book.douban.com/isbn/{}/'
session = requests.session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1)AppleWebKit'
                  '/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
}
login_douban_url = 'https://accounts.douban.com/login'
form = { 'redir': 'https://book.douban.com/', 'form_email': '13535853292', 'form_password': 'Admin123=456', 'login': '登录'}


def login_douban():
    """
    登录豆瓣
    注意有验证码与无验证码登录情况
    :return:
    """
    response = session.post(login_douban_url, data=form, headers=HEADERS)
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')
    captcha_url = soup.find('img', id="captcha_image")['src']
    reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
    captchaID = re.findall(reCaptchaID, page)
    captcha_img = session.get(captcha_url)
    f = open('captcha.png', 'wb')
    f.write(captcha_img.content)
    f.close()
    print("请查看本地验证码图片并输入验证码")
    captcha = input()
    form['captcha-solution'] = captcha
    form['captcha-id'] = captchaID
    session.post(login_douban_url, data=form, headers=HEADERS)


def douban_detail(isbn):
    """
    请求限制 每分钟40次
    :param isbn:
    :return:
    """
    book_detail = {}
    time.sleep(1)
    url = 'https://api.douban.com/v2/book/isbn/:{}'.format(isbn)
    response = session.get(url)

    response = json.loads(response.content.decode('utf-8'))
    try:
        if response['msg'] == 'book_not_found':
            return False
    except KeyError:
        pass
    try:
        book_detail['author'] = response['author'][0]
    except IndexError:
        print(url)
        # 只有ISBN, 没其他信息
        return False
    except KeyError:
        print(url)
        return False

    book_detail['author_intro'] = response['author_intro']
    book_detail['book_intro'] = response['summary']
    book_detail['book_price'] = response['price']
    book_detail['publisher'] = response['publisher']
    book_detail['isbn'] = response['isbn13']
    book_detail['title'] = response['title']
    book_detail['pages'] = response['pages']
    book_detail['book_img'] = response['images']['small']
    book_detail['subtitle'] = response['subtitle']
    book_detail['pub_date'] = response['pubdate']
    book_detail['book_catalog'] = response['catalog']

    return book_detail


def get_author(raw_author):
    parts = raw_author.split('\n')
    return ''.join(map(str.strip, parts))


def get_book_intro(line_tags):
    brief = line_tags[0].contents
    for tag in line_tags[1:]:
        brief += tag.contents
    brief = '\n'.join(brief)
    return brief


if __name__ == '__main__':
    login_douban()

