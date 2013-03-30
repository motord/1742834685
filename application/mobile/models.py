# -*- coding: utf-8 -*-
__author__ = 'peter'
from google.appengine.ext import ndb
from application.models import QRCode

class ScanRecord(ndb.Model):
    """Encapsulates information for a request log record."""

    method = ndb.StringProperty(required=True)
    qrcode = ndb.KeyProperty(QRCode, required=True)
    request_headers = ndb.StringProperty(repeated=True, indexed=False)
    status_code = ndb.IntegerProperty(required=True)
    status_text = ndb.StringProperty(required=True)
    response_headers = ndb.StringProperty(repeated=True, indexed=False)
    wall_time = ndb.IntegerProperty(required=True)
    cpu_time = ndb.IntegerProperty(required=True)
    random = ndb.FloatProperty(required=True)

    def to_json(self):
        """Returns a dict containing the relevant information from this record.

        Note that the return value is not a JSON string, but rather a dict that can
        be passed to a JSON library for encoding."""
        return dict((k, v.__get__(self, self.__class__)) for k, v in self.properties().iteritems())