# -*- coding: utf-8 -*-
__author__ = 'peter'

from application.models import Campaign, QRCode
from google.appengine.ext import deferred
from google.appengine.ext import ndb
import qrpress
from models import Registry
import StringIO
import logging

product=32
capacities = [2**x for x in range(0,6)]
code_url = 'http://qrcache.com/m/{0}'

def draft(key):
    campaign=key.get()
    qrcodes=[]
    for q in range(campaign.tally):
        qrcodes.append(QRCode(campaign=key))
    keys=ndb.put_multi(qrcodes)
    for k in keys:
        data=code_url.format(k.urlsafe())
        logging.info(data)
        code=k.get()
        alpha=StringIO.StringIO()
        qrpress.default_image('alpha', data).save(alpha)
        code.alpha=alpha.getvalue()
        alpha.close()
        beta=StringIO.StringIO()
        qrpress.default_image('beta', data).save(beta)
        code.beta=beta.getvalue()
        beta.close()
        gamma=StringIO.StringIO()
        qrpress.default_image('gamma', data).save(gamma)
        code.gamma=gamma.getvalue()
        gamma.close()
    keys=ndb.put_multi(qrcodes)
    campaign.qrcodes=keys
    campaign.put()
    q=Registry.query(Registry.capacity==campaign.tally)
    r=q.get()
    if not r:
        r=Registry(capacity=campaign.tally)
    r.campaigns.append(campaign.key)
    r.tally+=1
    r.put()

class Inventory(object):

    def __init__(self):
        pass

    def get_campaign(self, size):
        pass

    @classmethod
    def stock(self):
        holding=[]
        campaigns=[]
        for r in Registry.query().iter():
            h=r.capacity
            holding.append(h)
            if h in capacities:
                gap=product/r.capacity-r.tally
                for g in range(gap):
                    campaigns.append(Campaign(tally=h))
        missing=[c for c in capacities if c not in holding]
        for m in missing:
            for g in range(product/m):
                campaigns.append((Campaign(tally=m)))
        keys=ndb.put_multi(campaigns)
        for key in keys:
                deferred.defer(draft, key)

    def recycle(self):
        pass