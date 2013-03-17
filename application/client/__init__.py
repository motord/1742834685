# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template, flash, redirect, url_for
import logging
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from application.models import Campaign, QRCode

portal = Blueprint('portal', __name__, template_folder='templates')

@portal.route('/client/', methods=['GET'])
def home():
    return render_template('home.html')
