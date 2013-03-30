# -*- coding: utf-8 -*-
__author__ = 'peter'

from functools import wraps
from flask import redirect, request, abort, make_response
from google.appengine.ext import ndb
from application.models import QRCode
import logging
import time
import random
from models import ScanRecord
from google.appengine.api import quota

def _stringifyHeaders(header_dict):
    return ['%s: %s' % x for x in header_dict.items()]

def tracked(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        start_time = time.time()
        key=kwargs['key']
        logging.info('{0} tracked'.format(key))
        qrcode=kwargs['qrcode']
        response=make_response(func(*args, **kwargs))
        elapsed = int((time.time() - start_time) * 1000)
        record = ScanRecord(
            method=request.method,
            qrcode=key,
            request_headers=_stringifyHeaders(request.headers),
            status_code=int(response.status_code),
            status_text=response.status,
            response_headers=_stringifyHeaders(response.headers),
            wall_time=elapsed,
            cpu_time=quota.get_request_api_cpu_usage(),
            random=random.random()).put()
        return response
    return decorated_view
