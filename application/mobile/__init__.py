# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template, flash, redirect, url_for, make_response
import logging
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from application.models import Campaign, QRCode
from decorators import qrcode_required

scanner = Blueprint('scanner', __name__, template_folder='templates')

@scanner.route('/m/<string:key>', methods=['GET'])
@qrcode_required
def scan(qrcode, **kwargs):
    url=qrcode.redirect
    if url:
        return redirect(url)
    url=qrcode.campaign.redirect
    if url:
        return redirect(url)
    return render_template('hosting.html')

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
