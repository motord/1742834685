__author__ = 'peter'

from google.appengine.ext import ndb, deferred

class Slice(ndb.Model):
    content = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

class Block(ndb.Model):
    content = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

class BufferDB(ndb.Model):
    buffer_key = ndb.StringProperty(required=True)
    buffer_value=ndb.JsonProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)