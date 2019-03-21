import datetime

import requests
import json
from lib.base_user.base_user import BaseUser
from skimage import io,draw


class ReservationInfo(object):
    seat_host = "http://seat.lib.sdu.edu.cn"
    # 座位预约验证码URL
    seat_verify_url = "/api.php/check?"
    # 座位预约登录URL
    seat_login_url = "/api.php/login"
    # 图书馆座位预约首页
    lib_host = '/api.php/areas/{}'
    # 座位预约 选择预约时间URL
    reservation_time_url = "/api.php/space_days/{}"
    # 提交预约url
    reserve_seat_url = '/api.php/spaces/{}/book'
    # 座位分布图
    seat_img_url = '/Public/home/images/web/area/{}/seat-free.jpg'
    # 各图书馆预约URL
    lib_url = {
        '蒋震图书馆': seat_host + lib_host.format(1),
        '工学图书馆': seat_host + lib_host.format(12),
        '青岛图书馆': seat_host + lib_host.format(19),
        '中心文理分馆': seat_host + lib_host.format(61),
        '洪家楼图书馆': seat_host + lib_host.format(65),
        '兴隆山图书馆': seat_host + lib_host.format(73),
        '趵突泉图书馆': seat_host + lib_host.format(127),
    }
    #
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }

    def get_region(self, lib):
        """
            获取图书馆的楼层具体分布、数量
        :param lib: 1：蒋震图书馆
                    12：工学图书馆
                    19：青岛图书馆
                    61：中心文理分馆
                    65：洪家楼图书馆
                    73：兴隆山图书馆
                    127：趵突泉图书馆
        :return:{
                'result':
                'msg':
                'floor_region_list':
            }
        """
        lib_index_response = requests.get(self.lib_url[lib])
        lib_index_response = json.loads(lib_index_response.content.decode('utf-8'))
        floor_region_list = []
        if not lib_index_response['data']['list']['areaInfo']['isValid']:
            return {
                'result': False,
                'msg': '该图书馆不开放',
                'floor_region_list': 'No data'
            }
        else:
            areas = lib_index_response['data']['list']['childArea']
            for area in areas:
                region_list = []
                floor_region = {}
                if area['isValid']:
                    floor_response = requests.get(self.seat_host + '/api.php/areas/{}'.format(area['id']))
                    floor_response = json.loads(floor_response.content.decode('utf-8'))
                    child_areas = floor_response['data']['list']['childArea']
                    floor_region['floor'] = area['name']
                    # 选每层的区域 exm：D410信息共享大厅 D416蒋震馆社会科学书库...
                    for child_area in child_areas:
                        region_id = {}
                        if child_area['isValid']:
                            region_id['name'] = child_area['name']
                            region_id['id'] = child_area['id']
                            region_list.append(region_id)
                    if len(region_list):
                        floor_region['region'] = region_list
                        floor_region_list.append(floor_region)
            return {
                'result': True,
                'msg': '该图书馆开放',
                'region_list': floor_region_list,
            }

    def get_seat(self, select_date, region_id):
        session = requests.session()
        if select_date:
            date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            start_time = '08:00'
        else:
            date = datetime.date.today().strftime('%Y-%m-%d')
            start_time = datetime.datetime.now().strftime('%H:%M')

        space_time_buckets_response = session.get(
            self.seat_host + '/api.php/space_time_buckets?day={}&area={}'.format(date, region_id))
        space_time_buckets_response = json.loads(space_time_buckets_response.content.decode('utf-8'))
        segment = space_time_buckets_response['data']['list'][0]['bookTimeId']

        seat_free_img = session.get(self.seat_host + self.seat_img_url.format(region_id))
        f = open('/usr/SmartLibrary/static/seat_free_{}_{}.png'.format(region_id, date), 'wb')
        f.write(seat_free_img.content)
        f.close()
        seat_free_img = io.imread('/usr/SmartLibrary/static/seat_free_{}_{}.png'.format(region_id, date))

        space_seat_response = session.get(
            self.seat_host + '/api.php/spaces_old?area={}&segment={}&day={}&startTime={}&endTime=22:10'.format(region_id, segment, date, start_time))

        space_seat_response = json.loads(space_seat_response.content.decode('utf-8'))
        seats = space_seat_response['data']['list']
        seat_id = []
        seat_list = []
        has_appointed_seats = []
        for seat in seats:
            if int(seat['status']) == 1:
                # status = 2是已预约
                seat_id.append({'id': seat['id'], 'name': seat['name']})
                seat_list.append(seat['name'])
            else:
                has_appointed_seats.append(
                    {'x': seat['point_x'], 'y': seat['point_y'], 'height': seat['height'], 'width': seat['width']})

        if len(has_appointed_seats):
            for item in has_appointed_seats:
                x = item['x']
                width = item['width']
                y = item['y']
                height = item['height']
                rr, cc = draw.circle((y + height) * 7.4, (x + width) * 13.4, 18)
                draw.set_color(seat_free_img, [rr, cc], [96, 96, 96])

        io.imsave('/usr/SmartLibrary/static/seat_free_{}_{}.png'.format(region_id, date), seat_free_img)
        return {
            'result': True,
            'seat_list': seat_list,
            'seat_id': seat_id,
            'segment': segment,
            'seat_img': 'https://lib.lu2322.top/static/seat_free_{}_{}.png'.format(region_id, date),
            'date': date,
            'start_time': start_time,
            'select_date': select_date,
        }

    def reserve_seat(self, account, password, segment, seat):
        user = BaseUser(account=account, password=password)
        login_response, headers, access_token, student_id, session = user.login_lib_or_reservation()
        form = {'access_token': access_token, 'userid': student_id, 'segment': segment, 'type': '1'}
        reserve_response = session.post(self.seat_host + self.reserve_seat_url.format(seat), data=form, headers=self.HEADERS)
        reserve_response = json.loads(reserve_response.content.decode('utf-8'))
        return {
            'reserve_seat_msg': reserve_response['msg'],
            'result': True
        }
