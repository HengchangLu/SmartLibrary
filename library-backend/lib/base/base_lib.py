import json
from lib.base_exceptions import GreenException
from django.http import HttpResponse


def api_response(func):
    def wrapper(*args, **kw):
        try:
            response = func(*args, **kw)
        except GreenException as e:
            response = {'result': False, 'msg': str(e)}
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    return wrapper
