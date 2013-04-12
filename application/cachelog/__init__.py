# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template, flash, redirect, url_for, make_response
import logging
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from application.models import Campaign, QRCode
from application.mobile.decorators import qrcode_required

journal = Blueprint('journal', __name__, template_folder='templates')

@journal.route('/log/<string:key>', methods=['GET'])
@qrcode_required
def log(qrcode, **kwargs):
    return render_template('journal.html', qrcode=qrcode)