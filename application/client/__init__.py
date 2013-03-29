# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template, flash, redirect, url_for
import logging
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from decorators import profile_required

from application.models import Campaign, QRCode
from application.admin.warehouse import Inventory

portal = Blueprint('portal', __name__, template_folder='templates')

@portal.route('/client/', methods=['GET'])
@profile_required
def overview(profile):

    return render_template('overview.html', profile=profile)

@portal.route('/client/account', methods=['GET'])
@profile_required
def account(profile):

    return render_template('account.html', profile=profile)

@portal.route('/client/profile', methods=['GET'])
@profile_required
def profile(profile):

    return render_template('profile.html', profile=profile)

@portal.route('/client/support', methods=['GET'])
@profile_required
def support(profile):

    return render_template('support.html', profile=profile)

@portal.route('/api/campaign.json', methods=['GET'])
def campaign():
    return render_template('campaign.html')

@portal.route('/api/qrcode.json', methods=['GET'])
def qrcode():
    return render_template('qrcode.html')
