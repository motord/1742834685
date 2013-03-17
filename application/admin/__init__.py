# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template, flash, redirect, url_for
# from decorators import signature_verified, channel_required, bot_required
# from models import Channel, Message, Bot
# import choir
# import intepreter
import logging
from application.decorators import admin_required
# from forms import ChannelForm, BotForm
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from warehouse import Inventory
from application.support.models import Ticket
from application.client.models import Profile

bridge = Blueprint('bridge', __name__, template_folder='templates')

@bridge.route('/admin/', methods=['GET', 'POST'])
@admin_required
def panel():
    return render_template('panel.html')

@bridge.route('/admin/stock', methods=['GET', 'POST'])
@admin_required
def stock():
    pass
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