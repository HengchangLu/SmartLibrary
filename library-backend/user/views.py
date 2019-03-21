import logging
import os
from SmartLibrary import settings
from django.forms import model_to_dict
from .models import UserInfo, FeedbackInfo
from lib.base.base_lib import *
from lib.base.exceptions import *
from django.core.mail import send_mail
from lib.base_user.base_user import BaseUser
from lib.rsa.rsa import rsa_decrypt_time, create_new_keys
logging = logging.getLogger('django')
PUBLIC_FILE_PATH = os.path.join(settings.BASE_DIR, 'lib', 'rsa', 'public1.pem').replace('\\', '/')
SEAT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}


# 座位预约验证码URL
seat_verify_url = "http://seat.lib.sdu.edu.cn/api.php/check?"
# 座位预约登录URL
seat_login_url = "http://seat.lib.sdu.edu.cn/api.php/login"
# 书目检索系统、我的图书馆登录URL
# 302 重定向
mylib_login_url = "http://58.194.172.34/reader/redr_verify.php"
# 书目检索系统、我的图书馆验证码URL
mylib_verify_url = "http://58.194.172.34/reader/yz.php"
# 续借验证码
renew_verify_url = "http://58.194.172.34/reader/captcha.php"


def test_send_email(request):
    send_mail('Hello Mr Wang', 'Here is the message.', 'django@0bit.wang',
              ['yh@0bit.wang'], fail_silently=False)
    raise Exception()


@api_response
def login_lib_or_appoint(request):
    """
    url: login/appoint/seat/
    :param request:
            account: 校园卡账号
            password: 校园卡查询密码（rsa加密处理后的，需要进行解密）
    :return:response = {
                            'result'
                            'msg'
                            'user_info'
                        }
    """
    user_info = {}
    try:
        account = request.GET['account']
        password = request.GET['password']
    except Exception as e:
        raise RequestParamError(str(e))
    else:
        create_new_keys(1024)
        password = rsa_decrypt_time(password)
        user = BaseUser(account=account, password=password)
        login_response, _, _, _, _ = user.login_lib_or_reservation()

        try:
            user_info = UserInfo.objects.get(account=account)
            user_info = model_to_dict(user_info)
        except UserInfo.DoesNotExist:
            name = login_response['data']['list']['name']
            student_id = login_response['data']['list']['id']
            gender = login_response['data']['list']['gender']
            dept_name = login_response['data']['list']['deptName']
            user_info = {'name': name, 'student_id': student_id, 'gender': gender, 'dept_name': dept_name}
            UserInfo.objects.bulk_create(
                [UserInfo(name=name, student_id=student_id, gender=gender, dept_name=dept_name, account=int(account))]
                    )
        finally:
            response = {
                        'result': True,
                        'msg': '登录成功！',
                        'user_info': user_info,
                        }
            return response


@api_response
def get_feedback_msg(request):
    try:
        feedback_msg = request.GET['feedbackMsg']
        name = request.GET['name']
        gender = request.GET['gender']
        account = request.GET['account']
        student_id = request.GET['studentId']
        dept_name = request.GET['deptName']
    except Exception as e:
        raise RequestParamError(str(e))
    else:
        send_mail('山东大学智慧图书馆反馈意见提醒', feedback_msg, 'django@0bit.wang',
                  ['lh232200@163.com'], fail_silently=False)
        # FeedbackInfo.objects.bulk_create(
        #     [UserInfo(name=name, student_id=student_id, gender=gender, dept_name=dept_name, feedback_msg=feedback_msg, account=int(account))]
        # )
        response = {
            'result': True,
            'msg': '反馈信息提交成功!',
        }
        return response
