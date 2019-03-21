import rsa
import base64
from urllib import request
from datetime import datetime
from .exceptions import *
import os
from SmartLibrary import settings
PUBLIC_FILE_PATH = os.path.join(settings.BASE_DIR, 'lib', 'rsa', 'public1.pem').replace('\\', '/')
PRIVATE_FILE_PATH = os.path.join(settings.BASE_DIR, 'lib', 'rsa', 'private1.pem').replace('\\', '/')


def create_new_keys(lens):
    """
    生成的公/私钥均为pkcs1格式
    """
    public_key, private_key = rsa.newkeys(lens)
    with open('public1.pem', 'wb') as f:
        f.write(public_key.save_pkcs1())
    with open('private1.pem', 'wb') as f:
        f.write(private_key.save_pkcs1())


def rsa_encrypt(msg):
    """
        rsa加密
    """
    with open(PUBLIC_FILE_PATH, 'rb') as public_file:
        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_file.read())
    code = rsa.encrypt(msg.encode('utf-8'), public_key)
    code = base64.b64encode(code).decode('utf-8')
    code = request.quote(code)
    return code


def rsa_decrypt(code):
    """
        rsa解密
    """
    code = request.unquote(code)
    with open(PRIVATE_FILE_PATH, 'rb') as private_file:
        private_key = rsa.PrivateKey.load_pkcs1(private_file.read())
    code = base64.b64decode(code.encode('utf-8'))
    msg = rsa.decrypt(code, private_key).decode('utf-8')
    return msg


def rsa_encrypt_time(msg):
    time = str(int(datetime.now().timestamp()))
    msg = time + ',' + msg
    code = rsa_encrypt(msg)
    return code


def rsa_decrypt_time(code):
    try:
        code = rsa_decrypt(code)
        time_old = int(code.split(',')[0])
        time_new = int(datetime.now().timestamp())
    except Exception as e:
        raise RsaCodeFormatError(str(e))
    else:
        delta = time_new - time_old
        if delta / 60 < 3:
            return code.split(',')[1]
        else:
            raise RsaCodeExpired(code)


if __name__ == '__main__':
    s = '12345678'
    print(s)
    s = rsa_encrypt(s)
    print(s)
    s = rsa_decrypt(s)
    print(s)
