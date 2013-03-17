# -*- coding: utf-8 -*-
__author__ = 'peter'

from application.models import Campaign, QRCode
from google.appengine.ext import deferred

class Inventory(object):

    def __init__(self):
        pass

    def get_campaign(self, size):
        pass

    def stock(self):
        pass

    def recycle(self):
        pass