from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json


logger = logging.getLogger('django')


@csrf_exempt
def pull(request):
    if request.method == 'POST':
        hook = json.loads(request.body.decode('utf-8'))
        if hook['password'] == 'fjdkfajklfaljfl' and hook['hook_name'] == 'push_hooks':
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('127.0.0.1', 55555))
            sock.send(b'srhtstr')
            return HttpResponse('true')

    logger.info(json.loads(request.body.decode('utf-8')))


def page_error(request):
    response = {
        'result': False,
        'msg': '出错了'
    }
    return HttpResponse(json.dumps(response, ensure_ascii=False))

