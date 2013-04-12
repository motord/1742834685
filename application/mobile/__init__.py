# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template, flash, redirect, url_for, make_response
import logging
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from application.models import Campaign, QRCode
from decorators import qrcode_required
from tracker import tracked

scanner = Blueprint('scanner', __name__, template_folder='templates')

TARGET_CONVERSE = 1
TARGET_CDN = 2

def converse(qrcode):
    return redirect(url_for('journal.log', key=qrcode.key.urlsafe()))

@scanner.route('/m/<string:key>', methods=['GET'])
@qrcode_required
@tracked
def scan(qrcode, **kwargs):
    url=qrcode.redirect
    if url:
        return redirect(url)
    url=qrcode.campaign.get().redirect
    if url:
        return redirect(url)
    if qrcode.target:
        return {TARGET_CONVERSE: converse}[qrcode.target](qrcode)
    return redirect(url_for('plea.claim', key=qrcode.key))

@scanner.route('/alpha/<string:key>', methods=['GET'])
@qrcode_required
def alpha(qrcode, **kwargs):
    response=make_response(qrcode.alpha)
    response.headers['Content-Type'] = 'image/png'
    return response

@scanner.route('/beta/<string:key>', methods=['GET'])
@qrcode_required
def beta(qrcode, **kwargs):
    response=make_response(qrcode.beta)
    response.headers['Content-Type'] = 'image/png'
    return response

@scanner.route('/gamma/<string:key>', methods=['GET'])
@qrcode_required
def gamma(qrcode, **kwargs):
    response=make_response(qrcode.gamma)
    response.headers['Content-Type'] = 'image/png'
    return response
