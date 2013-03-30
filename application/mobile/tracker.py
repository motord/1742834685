# -*- coding: utf-8 -*-
__author__ = 'peter'

from functools import wraps
from flask import redirect, request, abort
from google.appengine.ext import ndb
from application.models import QRCode
import logging

def tracked(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        key=kwargs['key']
        logging.info('{0} tracked'.format(key))
        qrcode=kwargs['qrcode']
        return func(*args, **kwargs)
    return decorated_view
