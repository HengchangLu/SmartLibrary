from lib.base_exceptions import RedException, GreenException


class RequestParamError(RedException):
    """
    请求参数错误
    """
    def __init__(self, param):
        msg = '请求' + param + '参数出错'
        RedException.__init__(self, msg)
