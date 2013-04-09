# -*- coding: utf-8 -*-
__author__ = 'peter'

from functools import wraps
from flask import redirect, request, abort
from google.appengine.ext import ndb
from application.models import QRCode

def qrcode_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        key=ndb.Key(urlsafe=kwargs['key'])
        kwargs['key']=key
        qrcode=key.get()
        kwargs['qrcode']=qrcode
        return func(*args, **kwargs)
    return decorated_view

def campaign_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        key=ndb.Key(urlsafe=kwargs['key'])
        kwargs['key']=key
        campaign=key.get()
        kwargs['campaign']=campaign
        return func(*args, **kwargs)
    return decorated_view
