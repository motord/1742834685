# -*- coding: utf-8 -*-
__author__ = 'peter'

from flask import Blueprint, request, Response, render_template, flash, redirect, url_for, current_app, json
import logging
from application.decorators import admin_required
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from warehouse import inventory
from models import Registry
from application.support.models import Ticket
from application.client.models import Profile
from google.appengine.ext.ndb import Key
from simmetrica import olap
from simmetrica.keeper import Keeper

bridge = Blueprint('bridge', __name__, template_folder='templates')

@bridge.route('/admin/', methods=['GET', 'POST'])
@admin_required
def panel():
    # q=Registry.query().iter()
    return render_template('dashboard.html', bucket_count=inventory.bucket_count())

@bridge.route('/admin/stock', methods=['POST'])
@admin_required
def stock():
    inventory.stock()
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
    # inventory.bucket()
    data=Keeper.read()
    if len(data)>0:
        request_body=render_template('bigquery.request.body', data=data)
        olap.syncdb(request_body)
    return 'OK'

@bridge.route('/admin/sow', methods=['GET'])
def sow():
    qrcode=Key(urlsafe='aglzfmsyY2FjaGVyDgsSBlFSQ29kZRilsCQM').get()
    qrcode.note=u'那一天我二十一岁，在我一生的黄金时代。我有好多奢望。我想爱，想吃，还想在一瞬间变成天上半明半暗的云。后来我才知道，生活就是个缓慢受锤的过程，人一天天老下去，奢望也一天天消失，最后变得像挨了锤的牛一样。可是我过二十一岁生日时没有预见到这一点。我觉得自己会永远生猛下去，什么也锤不了我。'
    qrcode.target=1
    qrcode.put()
    return 'OK'
