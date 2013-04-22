#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from google.appengine.ext import ndb, deferred
from google.appengine.api import memcache
from keeper import Keeper
from models import BufferDB
from settings import CACHE_TIMEOUT, CACHE_KEY
from decorators import cached

def prepare_query(sql, cache_key):
    rv={'timeline':[{'timestamp':1366525800, 'scans':172},
                    {'timestamp':1366525740, 'scans':148},
                    {'timestamp':1366525680, 'scans':121},
                    {'timestamp':1366525620, 'scans':76},
                    {'timestamp':1366525560, 'scans':34},
                    {'timestamp':1366525860, 'scans':3},
                    {'timestamp':1366525500, 'scans':6}]}
    buffer=BufferDB.query(BufferDB.buffer_key==cache_key).get()
    if not buffer:
        buffer=BufferDB(buffer_key=cache_key)
    buffer.buffer_value=rv
    buffer.put()
    memcache.set(cache_key, rv, time=CACHE_TIMEOUT)

class Simmetrica(object):

    DEFAULT_RESOLUTION = '5min'

    resolutions = {
        'min': 60,
        '5min': 300,
        '15min': 900,
        'hour': 3600,
        'day': 86400,
        'week': 86400 * 7,
        'month': 86400 * 30,
        'year': 86400 * 365
    }

    def __init__(self, host=None, port=None, db=None, password=None):
        pass

    @ndb.transactional
    def push(self, template, event, now=None):
        entries=[]
        for resolution, timestamp in self.get_timestamps_for_push(now):
            entries.append(self.get_event_entry(template, event, resolution, timestamp))
        Keeper.write(entries)

    @cached()
    def query(self, sql):
        cache_key=CACHE_KEY.format(hash(sql))
        buffer=BufferDB.query(BufferDB.buffer_key==cache_key).get()
        rv=buffer.buffer_value if buffer else None
        deferred.defer(prepare_query, sql, cache_key)
        return rv

    def get_timestamps_for_push(self, now):
        now = now or self.get_current_timestamp()
        for resolution, timestamp in self.resolutions.items():
            yield resolution, self.round_time(now, timestamp)

    def round_time(self, time, resolution):
        return int(time - (time % resolution))

    def get_event_entry(self, template, event, resolution, timestamp):
        return template.format(event, resolution, timestamp)

    def get_current_timestamp(self):
        return int(time.time())

    def syncdb(self):
        pass