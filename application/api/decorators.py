# -*- coding: utf-8 -*-
__author__ = 'peter'

from functools import wraps
from flask import redirect, request, abort
from google.appengine.ext import ndb
from application.models import QRCode
