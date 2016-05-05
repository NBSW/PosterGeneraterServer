# coding: utf-8
from django.http.response import HttpResponse
import json
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import time

class JsonResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
	logging.info("return  "+args[0])
	logging.info("------------------------------------------------------------------------------------")
        super(JsonResponse,self).__init__(content_type='application/json;charset=utf-8',*args,**kwargs)

def json_view(func):
    def _wrapper(*args, **kwargs):
        rst = func(*args, **kwargs)
        if isinstance(rst, (dict, list)):
            rst = json.dumps(rst,ensure_ascii=False)    
            return JsonResponse(rst)
        return rst
    return _wrapper
