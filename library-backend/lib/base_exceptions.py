class DjangoException(Exception):
    """
    自定义异常父类
    """
    def __init__(self, msg):
        Exception.__init__(self, msg)


class RedException(DjangoException):
    """
    红色异常，直接从Django抛出
    """
    def __init__(self, msg="Unknown Error"):
        DjangoException.__init__(self, msg)


class GreenException(DjangoException):
    """
    绿色异常，将异常信息作为msg返回
    """
    def __init__(self, msg):
        DjangoException.__init__(self, msg)