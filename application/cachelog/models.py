__author__ = 'peter'

from google.appengine.ext import ndb
from application.models import Campaign

class Template(ndb.Model):
    email = ndb.TextProperty(required=True)
    mockup = ndb.BlobProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
