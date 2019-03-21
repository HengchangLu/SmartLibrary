import re

import requests
from bs4 import BeautifulSoup
from lib.solve_captchas_with_model import get_verify_via_model
from lib.solve_captchas_with_OCR import get_verify_via_ocr
import json
from .exceptions import *


class BaseUser(object):
    # 座位预约验证码URL
    seat_verify_url = "/api.php/check?"
    # 座位预约登录URL
    seat_login_url = "/api.php/login"
    # 书目检索系统、我的图书馆登录URL
    mylib_login_url = "/redr_verify.php"  # 302 重定向
    # 书目检索系统、我的图书馆验证码URL
    mylib_verify_url = "/yz.php"
    # 续借验证码
    renew_verify_url = "/captcha.php"
    # HEADERS
    SEAT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    MYLIB_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '48',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': '58.194.172.34',
        'Origin': 'http://58.194.172.34',
        'Referer': 'http://58.194.172.34/reader/login.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    seat_host = 'http://seat.lib.sdu.edu.cn'
    mylib_host = 'http://58.194.172.34/reader'

    def __init__(self, account, password):
        self.account = account
        self.password = password

    def login_lib_or_reservation(self):
        """
        登录图书馆 同时也是登录座位预约
        :return: 登录情况
        """
        global verify
        while True:
            session = requests.session()
            verify_img = session.get(self.seat_host + self.seat_verify_url)
            f = open('/usr/SmartLibrary/user/static/reservation_captchas/check.png', 'wb')
            f.write(verify_img.content)
            f.close()
            verify = get_verify_via_model()
            form = {'username': self.account, 'password': self.password, 'verify': verify}
            HEADERS = self.SEAT_HEADERS
            login_response = session.post(self.seat_host + self.seat_login_url, data=form, headers=HEADERS)
            headers = login_response.headers
            login_response = json.loads(login_response.content.decode('utf-8'))
            if login_response['msg'] == "验证码错误，请重新输入":
                continue
            elif login_response['msg'] == "登陆成功":
                access_token = re.findall(r'access_token=(.*?); ', str(headers['Set-Cookie']))[0]
                student_id = login_response['data']['list']['id']
                return login_response, headers, access_token, student_id, session
            elif login_response['msg'] == "":
                raise LoginFailure(self.account)

    def login_mylib(self):
        """
        登录我的图书馆(书目检索系统)、获取借阅信息
        :return:
        """
        global verify
        while True:
            session = requests.session()
            verify_img = session.get(self.mylib_host + self.mylib_verify_url)
            f = open('/usr/SmartLibrary/user/static/mylib_captchas/check.png', 'wb')
            f.write(verify_img.content)
            f.close()
            verify = get_verify_via_ocr('/usr/SmartLibrary/user/static/mylib_captchas/check.png')
            form = {'number': self.account, 'passwd': self.password, 'code': verify}
            HEADERS = self.MYLIB_HEADERS
            login_response = session.post(self.mylib_host + self.mylib_login_url, data=form, headers=HEADERS)
            # headers = login_response.headers
            login_response.encoding = 'utf-8'
            login_response_soup = BeautifulSoup(login_response.text, 'html.parser')
            login_response_msg = login_response_soup.select('font[color="red"]')
            # return login_response_msg, time
            # if login_response_msg:
            #     # time = time + 1
            #     continue
            #     # return str(login_response_msg), time
            # else:
            #     return session, time
            while not login_response_msg:
                return session


