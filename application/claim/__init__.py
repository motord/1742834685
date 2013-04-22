# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template, flash, redirect, url_for, make_response
import logging
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from application.models import Campaign, QRCode
from application.mobile.decorators import qrcode_required
from decorators import upyun_packaged, UPYUN_BUCKET, UPYUN_URL, upyun_bumper
from application.client.decorators import profile_required
from application.mobile import TARGET_REDIRECT, TARGET_CONVERSE, TARGET_CDN
from google.appengine.ext import ndb

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
    if 'redirect' in request.form:
        qrcode.redirect=request.form['redirect']
        qrcode.target=TARGET_REDIRECT
        key=inbox_collect(qrcode, profile).put()
        return redirect(url_for('portal.qrcode', key=key.urlsafe()))
    else:
        qrcode.target=TARGET_CONVERSE
        qrcode.redirect=None
        qrcode.note=request.form['note']
        key=inbox_collect(qrcode, profile).put()
        return redirect(url_for('journal.log', key=key.urlsafe()))

@ndb.transactional
def inbox_collect(qrcode, profile):
    if qrcode.campaign not in profile.campaigns:
        giver=qrcode.campaign.get()
        giver.qrcodes.remove(qrcode.key)
        giver.tally-=1
        giver.put()
        receiver=profile.inbox
        qrcode.campaign=receiver
        inbox=receiver.get()
        inbox.qrcodes.append(qrcode.key)
        inbox.tally+=1
        inbox.put()
    return qrcode

@plea.route('/claim/upyun/notify', methods=['POST'])
@upyun_bumper
def upyun_notify():
    return 'OK'

@plea.route('/claim/upyun/return', methods=['GET'])
@upyun_bumper
def upyun_return(key):
    return redirect(url_for('portal.qrcode', key=key))
