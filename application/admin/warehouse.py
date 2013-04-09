# -*- coding: utf-8 -*-
__author__ = 'peter'

from application.models import Campaign, QRCode
from google.appengine.ext import deferred
from google.appengine.ext import ndb
import qrpress
from models import Registry, Bucket
import StringIO
import logging
import random
from application.decorators import cached

PRODUCT=32
CAPACITIES = [2**x for x in range(0,6)]
CODE_URL = 'http://qrcache.com/m/{0}'
NUM_SHARDS = 256
BUCKET_SIZE = 4

class Inventory(object):

    def __init__(self):
        pass

    def get_campaign(self, size):
        pass

    @staticmethod
    def draft(key):
        campaign=key.get()
        qrcodes=[]
        for q in range(campaign.tally):
            qrcodes.append(QRCode(campaign=key))
        keys=ndb.put_multi(qrcodes)
        keys=Inventory.assemble(keys)
        campaign.qrcodes=keys
        campaign.put()
        q=Registry.query(Registry.capacity==campaign.tally)
        r=q.get()
        if not r:
            r=Registry(capacity=campaign.tally)
        r.campaigns.append(campaign.key)
        r.tally+=1
        r.put()

    @staticmethod
    def assemble(keys):
        qrcodes=[]
        for k in keys:
            data=CODE_URL.format(k.urlsafe())
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
            qrcodes.append(code)
        return ndb.put_multi(qrcodes)

    def stock(self):
        holding=[]
        campaigns=[]
        for r in Registry.query().iter():
            h=r.capacity
            holding.append(h)
            if h in CAPACITIES:
                gap=PRODUCT/r.capacity-r.tally
                for g in range(gap):
                    campaigns.append(Campaign(tally=h))
        missing=[c for c in CAPACITIES if c not in holding]
        for m in missing:
            for g in range(PRODUCT/m):
                campaigns.append((Campaign(tally=m)))
        keys=ndb.put_multi(campaigns)
        for key in keys:
                deferred.defer(Inventory.draft, key)

    def recycle(self):
        pass

    @staticmethod
    @cached(key='bucket_count')
    def bucket_count():
        total=0
        for bucket in Bucket.query():
            total += bucket.headcount
        return total

    def bucket(self):
        qrcodes=[]
        for q in range(BUCKET_SIZE):
            qrcodes.append(QRCode())
        keys=ndb.put_multi(qrcodes)
        keys=Inventory.assemble(keys)
        shard_string_index = str(random.randint(0, NUM_SHARDS - 1))
        bucket = Bucket.get_by_id(shard_string_index)
        if bucket is None:
            bucket = Bucket(id=shard_string_index)
        bucket.headcount += len(keys)
        bucket.qrcodes=keys
        bucket.put()

    def alloc(self, campaign_key, n):
        keys=[]
        remainder=n
        for bucket in Bucket.query():
            available=len(bucket.qrcodes)
            if available>=remainder:
                keys.extend(bucket.qrcodes[:remainder])
                bucket.qrcodes=bucket.qrcodes[remainder:]
                bucket.headcount-=remainder
                bucket.put()
                qrcodes=[]
                for key in keys:
                    qrcode=key.get()
                    qrcode.campaign=campaign_key
                    qrcodes.append(qrcode)
                keys=ndb.put_multi(qrcodes)
                campaign=campaign_key.get()
                campaign.qrcodes.extend(keys)
                campaign.tally+=len(keys)
                campaign.put()
                return keys
            else:
                remainder-=available
                keys.extend(bucket.qrcodes)
                bucket.qrcodes=[]
                bucket.headcount=0
                bucket.put()


inventory = Inventory()
