#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random
from google.appengine.ext import ndb, deferred

NUM_SHARDS = 16

class Slice(ndb.Model):
    content = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

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
        shard_string_index = str(random.randint(0, NUM_SHARDS - 1))
        slice = Slice.get_by_id(shard_string_index)
        if slice is None:
            slice = Slice(id=shard_string_index)
        if slice.content:
            entries.append(slice.content)
        slice.content = '\r\n'.join(entries)
        slice.put()


    def query(self, event, start, end, resolution=DEFAULT_RESOLUTION):
        key = self.get_event_key(event, resolution)
        timestamps = self.get_timestamps_for_query(
            start, end, self.resolutions[resolution])
        values = self.backend.hmget(key, timestamps)
        for timestamp, value in zip(timestamps, values):
            yield timestamp, value or 0

    def get_timestamps_for_query(self, start, end, resolution):
        return range(self.round_time(start, resolution),
                     self.round_time(end, resolution),
                     resolution)

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
