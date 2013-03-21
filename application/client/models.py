__author__ = 'peter'

from google.appengine.ext import ndb

class Profile(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    credit = ndb.IntegerProperty(required=True)
    campaigns = ndb.KeyProperty(repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
