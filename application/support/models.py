__author__ = 'peter'

from google.appengine.ext import ndb
from application.client.models import Profile

class Ticket(ndb.Model):
    profile=ndb.KeyProperty(Profile)
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
