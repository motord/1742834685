# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template, flash, redirect, url_for, current_app, json
# from decorators import signature_verified, channel_required, bot_required
# from models import Channel, Message, Bot
# import choir
# import intepreter
import logging
from application.decorators import admin_required
# from forms import ChannelForm, BotForm
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from application.admin.models import Registry
from application.support.models import Ticket
from application.client.models import Profile
from application.mobile.decorators import campaign_required
from application.mobile.decorators import qrcode_required

cruncher = Blueprint('cruncher', __name__, template_folder='templates')

@cruncher.route('/api/<string:key>.campaign', methods=['GET'])
@campaign_required
@admin_required
def campaign(campaign, **kwargs):
    q=Registry.query().iter()
    lineitems=[]
    for lineitem in q:
        lineitems.append({'capacity' : lineitem.capacity, 'tally' : lineitem.tally})
    return current_app.response_class(json.dumps(lineitems, indent=None if request.is_xhr else 2), mimetype='application/json')

@cruncher.route('/api/<string:key>.qrcodes', methods=['GET'])
@campaign_required
@admin_required
def qrcodes(campaign, **kwargs):
    qrcodes=campaign.qrcodes
    return current_app.response_class(json.dumps(qrcodes, indent=None if request.is_xhr else 2), mimetype='application/json')

@cruncher.route('/api/<string:key>.qrcode', methods=['GET'])
@qrcode_required
@admin_required
def qrcode(qrcode, **kwargs):
    q=Registry.query().iter()
    lineitems=[]
    for lineitem in q:
        lineitems.append({'capacity' : lineitem.capacity, 'tally' : lineitem.tally})
    return current_app.response_class(json.dumps(lineitems, indent=None if request.is_xhr else 2), mimetype='application/json')

@cruncher.route('/api/<string:key>.tags', methods=['GET'])
@qrcode_required
@admin_required
def tags(qrcode, **kwargs):
    tags=qrcode.tags
    return current_app.response_class(json.dumps(tags, indent=None if request.is_xhr else 2), mimetype='application/json')

@cruncher.route('/api/registry.json', methods=['GET'])
@admin_required
def registry():
    q=Registry.query().iter()
    lineitems=[]
    for lineitem in q:
        lineitems.append({'capacity' : lineitem.capacity, 'tally' : lineitem.tally})
    return current_app.response_class(json.dumps(lineitems, indent=None if request.is_xhr else 2), mimetype='application/json')