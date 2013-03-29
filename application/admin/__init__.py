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

from warehouse import Inventory
from models import Registry
from application.support.models import Ticket
from application.client.models import Profile

bridge = Blueprint('bridge', __name__, template_folder='templates')

@bridge.route('/admin/', methods=['GET', 'POST'])
@admin_required
def panel():
    q=Registry.query().iter()
    return render_template('dashboard.html', lineitems=q, bucket_count=Inventory.bucket_count())

@bridge.route('/api/registry.json', methods=['GET'])
@admin_required
def registry():
    q=Registry.query().iter()
    lineitems=[]
    for lineitem in q:
        lineitems.append({'capacity' : lineitem.capacity, 'tally' : lineitem.tally})
    return current_app.response_class(json.dumps(lineitems, indent=None if request.is_xhr else 2), mimetype='application/json')

@bridge.route('/admin/stock', methods=['POST'])
@admin_required
def stock():
    Inventory.stock()
    flash(u'Stock replenishment started.', 'success')
    return redirect(url_for('bridge.panel'))
    # remark = intepreter.parse(request.data)
    # message=Message(channel=channel.key, from_user=remark['fromUser'],
    #                 to_user=remark['toUser'], create_time=remark['createTime'],
    #                 message_type=remark['msgType'], message=remark['message'])
    # message.put()
    # remark['channel']=channel
    # retort=choir.chant(remark)
    # message=Message(channel=channel.key, from_user=retort['fromUser'],
    #                 to_user=retort['toUser'], create_time=retort['createTime'],
    #                 message_type=retort['msgType'], message=retort['message'])
    # message.put()
    # return Response(retort['message'], content_type='application/xml;charset=utf-8')

@bridge.route('/admin/heartbeat', methods=['GET'])
def heartbeat():
    Inventory.bucket()
    return 'OK'