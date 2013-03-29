__author__ = 'peter'

from google.appengine.ext import ndb

class Profile(ndb.Model):
    user=ndb.UserProperty(required=True)
    nickname = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    credit = ndb.IntegerProperty(default=2)
    campaigns = ndb.KeyProperty(repeated=True)
    tickets= ndb.KeyProperty(repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
