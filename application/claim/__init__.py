# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template, flash, redirect, url_for, make_response
import logging
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from application.models import Campaign, QRCode
from application.mobile.decorators import qrcode_required

plea = Blueprint('plea', __name__, template_folder='templates')

@plea.route('/claim/<string:key>', methods=['GET'])
@qrcode_required
def scan(qrcode, **kwargs):
    url=qrcode.redirect
    if url:
        return redirect(url)
    url=qrcode.campaign.redirect
    if url:
        return redirect(url)
    return render_template('claim.html')