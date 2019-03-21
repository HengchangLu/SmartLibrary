from lib.base_exceptions import RedException


class RsaCodeIsNotValid(RedException):
    """
    RSA加密信息无效
    初始化参数：消息
    """
    def __init__(self, msg):
        RedException.__init__(self, msg)


class RsaCodeFormatError(RsaCodeIsNotValid):
    """
    RSA加密信息格式有误
    """
    def __init__(self, rsa_msg):
        msg = 'RSA加密信息格式有误，msg:' + rsa_msg
        RsaCodeIsNotValid.__init__(self, msg)


class RsaCodeExpired(RsaCodeIsNotValid):
    """
    RSA加密信息过期
    """
    def __init__(self, rsa_msg):
        msg = "RSA加密信息过期，msg：" + rsa_msg
        RsaCodeIsNotValid.__init__(self, msg)


class RsaCodeNotMatch(RsaCodeIsNotValid):
    """
    RSA加密信息不匹配
    """
    def __init__(self, rsa_msg):
        msg = "RSA加密信息不匹配， msg：" + rsa_msg
        RsaCodeIsNotValid.__init__(self, msg)
