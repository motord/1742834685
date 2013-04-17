# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template, flash, redirect, url_for, make_response
import logging
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from application.models import Campaign, QRCode
from application.mobile.decorators import qrcode_required
from decorators import upyun_packaged, UPYUN_BUCKET, UPYUN_URL
from application.client.decorators import profile_required
from application.mobile import TARGET_CONVERSE, TARGET_CDN
import re
from google.appengine.ext.ndb import Key

plea = Blueprint('plea', __name__, template_folder='templates')

@plea.route('/claim/<string:key>', methods=['GET'])
@profile_required
@qrcode_required
@upyun_packaged
def claim(qrcode, upyun, profile, **kwargs):
    return render_template('claim.html', qrcode=qrcode, upyun=upyun, profile=profile)

@plea.route('/claim/<string:key>', methods=['POST'])
@profile_required
@qrcode_required
def turf(qrcode, profile, **kwargs):
    qrcode.target=TARGET_CONVERSE
    qrcode.redirect=None
    qrcode.note=request.form['note']
    if not qrcode.campaign:
        qrcode.campaign=profile.inbox
        inbox=profile.inbox.get()
        inbox.qrcodes.append(qrcode.key)
        inbox.tally+=1
        inbox.put()
    qrcode.put()
    return redirect(url_for('journal.log', key=qrcode.key.urlsafe()))


@plea.route('/claim/upyun/notify', methods=['POST'])
def upyun_notify():
    code=request.form['code']
    message=request.form['message']
    url=request.form['url']
    time=request.form['time']
    # sign=request.form['sign']
    logging.info(url)
    m = re.match(r'/(.*)/(.*)\.(.*)', url)
    if m:
        campaign=Key(urlsafe=m.group(1)).get()
        qrcode=Key(urlsafe=m.group(2)).get()
        suffix=m.group(3)
        qrcode.redirect=UPYUN_URL.format(UPYUN_BUCKET, m.group(1), m.group(2), suffix)
        qrcode.target=TARGET_CDN
        qrcode.put()
    return 'OK'

@plea.route('/claim/upyun/return', methods=['GET'])
def upyun_return():
    code=request.args['code']
    message=request.args['message']
    url=request.args['url']
    time=request.args['time']
    # sign=request.args['sign']
    logging.info(url)
    m = re.match(r'/(.*)/(.*)\.(.*)', url)
    if m:
        campaign=Key(urlsafe=m.group(1)).get()
        qrcode=Key(urlsafe=m.group(2)).get()
        suffix=m.group(3)
        qrcode.redirect=UPYUN_URL.format(UPYUN_BUCKET, m.group(1), m.group(2), suffix)
        qrcode.target=TARGET_CDN
        qrcode.put()
        return redirect(url_for('portal.qrcode', key=m.group(2)))
