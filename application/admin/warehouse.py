# -*- coding: utf-8 -*-
__author__ = 'peter'

from application.models import Campaign, QRCode
from google.appengine.ext import deferred
from google.appengine.ext import ndb

product=1024
capacities = [2**x for x in range(1,10)]

class Registry(ndb.Model):
    capacity = ndb.IntegerProperty(required=True)
    campaigns = ndb.KeyProperty(repeated=True)
    tally = ndb.IntegerProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

def draft(campaign):
    qrcodes=[]
    for q in range(campaign.tally):
        qrcodes.append(QRCode(campaign=campaign))
    keys=ndb.put_multi(qrcodes)
    campaign.qrcodes=keys
    campaign.put()
    q=Registry.query(Registry.capacity==campaign.tally)
    r=q.get()
    if not r:
        r=Registry(capacity=campaign.tally)
    r.campaigns.append(campaign)
    r.tally+=1
    r.put()

class Inventory(object):

    def __init__(self):
        pass

    def get_campaign(self, size):
        pass

    def stock(self):
        holding=[]
        campaigns=[]
        for r in Registry.query():
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
        for campaign in campaigns:
                deferred.defer(draft, campaign)

    def recycle(self):
        pass