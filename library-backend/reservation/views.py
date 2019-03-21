from .lib.reservation_info import ReservationInfo
from lib.base.base_lib import *
from lib.base.exceptions import *


@api_response
def get_region(request):
    """
     获取区域分布信息
    :param request:
            lib:   每个图书馆的编号
    URL: http://seat.lib.sdu.edu.cn/api.php/login
    :return: floor_region
    """
    try:
        lib = request.GET['lib']
    except Exception as e:
        raise RequestParamError(str(e))
    else:
        region = ReservationInfo()
        return region.get_region(lib)


@api_response
def get_seat(request):
    """
    获取对应区域座位分布图
    :param request:
                select_date： 选择预约的时间
                region_id: 区域的ID
    :return:
        {
            'result': booleans
            'seat_list':
            'seat_id':
            'segment':
            'seat_img':
            'date':
            'start_time':
            'select_date':
        }
    """
    try:
        select_date = int(request.GET['selectDate'])
        region_id = request.GET['regionId']
    except Exception as e:
        raise RequestParamError(str(e))
    else:
        seat = ReservationInfo()
        return seat.get_seat(select_date, region_id)


@api_response
def reserve_seat(request):
    """
    申请预约座位
    :param request:
                account：校园卡账号800547
                password: 校园卡查询密码
                segment: 类似于区域的Id
                seat: 用户选择的位置
    :return:
    """
    try:
        account = request.GET['account']
        password = request.GET['password']
        segment = request.GET['segment']
        seat = request.GET['seat']
    except Exception as e:
        raise RequestParamError(str(e))
    else:
        user = ReservationInfo()
        return user.reserve_seat(account, password, segment, seat)

