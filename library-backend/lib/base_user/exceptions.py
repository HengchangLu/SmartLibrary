from lib.base_exceptions import RedException, GreenException


class LoginFailure(GreenException):
    """
    用户登录图书馆(分两种情况：座位预约登录和我的图书馆登录)失败
    """
    def __init__(self, username):
        msg = username + '用户名或者密码错误!'
        GreenException.__init__(self, msg)


class LibNoAccess(RedException):
    """
    用户登录图书馆(分两种情况：座位预约登录和我的图书馆登录)失败
    """
    def __init__(self):
        msg = "图书馆拒绝访问！"
        RedException.__init__(self, msg)
