# -*- coding: utf-8 -*-
__author__ = 'peter'

from functools import wraps
from flask import redirect, request, abort
from google.appengine.ext import ndb
from application.models import QRCode
import time
from application.upyun import md5
import base64
from flask import json
import logging
from application.mobile import TARGET_REDIRECT, TARGET_CONVERSE, TARGET_CDN
import re
from google.appengine.ext.ndb import Key
from google.appengine.api import memcache

UPYUN_API_KEY='/QCoz1YOtYHXpQi/FosDECPhkG0='
UPYUN_BUCKET='qrcache'
UPYUN_URL='http://{0}.b0.upaiyun.com/{1}/{2}.{3}'
UPYUN_NOTIFY_URL='http://www.qrcache.com/claim/upyun/notify'
UPYUN_RETURN_URL='http://www.qrcache.com/claim/upyun/return'

def upyun_packaged(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        qrcode=kwargs['qrcode']
        file=qrcode.key.urlsafe()
        folder=qrcode.campaign.urlsafe()
        expiration = int(time.time()+600)
        policydoc = {'bucket':UPYUN_BUCKET,
                     'return-url':UPYUN_RETURN_URL,
                     'notify-url':UPYUN_NOTIFY_URL,
                     'expiration':expiration,
                     'save-key':'/{0}/{1}'.format(folder, file)+'{.suffix}',
                     # 'allow-file-type':'jpg,jpeg,gif,png',
                     'content-lenth-range':'0,10240000',
                     }
        logging.info(policydoc)
        policy = base64.encodestring(json.dumps(policydoc))
        policy = ''.join(policy.split())
        logging.info(policy)
        signature = md5(policy+"&"+UPYUN_API_KEY)
        kwargs['upyun']={'policy':policy, 'signature':signature, 'bucket':UPYUN_BUCKET}
        return func(*args, **kwargs)
    return decorated_view

def upyun_bumper(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method=='POST':
            code=request.form['code']
            message=request.form['message']
            url=request.form['url']
            time=request.form['time']
            # sign=request.form['sign']
        else:
            code=request.args['code']
            message=request.args['message']
            url=request.args['url']
            time=request.args['time']
            # sign=request.args['sign']
        logging.info(url)
        m = re.match(r'/(.*)/(.*)\.(.*)', url)
        if m:
            key=m.group(2)
            v=memcache.get(key)
            if v and v==url:
                logging.info('bump')
            else:
                campaign=Key(urlsafe=m.group(1)).get()
                qrcode=Key(urlsafe=key).get()
                suffix=m.group(3)
                qrcode.redirect=UPYUN_URL.format(UPYUN_BUCKET, m.group(1), m.group(2), suffix)
                qrcode.target=TARGET_CDN
                qrcode.put()
                memcache.set(key, url)
            kwargs['key']=key
        return func(*args, **kwargs)
    return decorated_view