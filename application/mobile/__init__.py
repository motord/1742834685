# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template, flash, redirect, url_for
import logging
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from application.models import Campaign, QRCode

scanner = Blueprint('scanner', __name__, template_folder='templates')

@scanner.route('/m/<string:key>', methods=['GET'])
def scan(key):
    pass
