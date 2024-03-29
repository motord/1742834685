__author__ = 'peter'

from google.appengine.ext import ndb

class Registry(ndb.Model):
    capacity = ndb.IntegerProperty(required=True)
    campaigns = ndb.KeyProperty(repeated=True)
    tally = ndb.IntegerProperty(default=0)
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

class Bucket(ndb.Model):
    headcount = ndb.IntegerProperty(default=0)
    qrcodes = ndb.KeyProperty(repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

class Lead(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)