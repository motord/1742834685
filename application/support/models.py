__author__ = 'peter'

from google.appengine.ext import ndb

class Ticket(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
