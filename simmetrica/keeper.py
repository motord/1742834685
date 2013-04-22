__author__ = 'peter'

from google.appengine.api import memcache
from settings import WRITE_BLOCK, NUM_SHARDS, SHARD_STRING_INDEX, USE_MEMCACHE_KEEPER, USE_SLICE_KEEPER
import random
from google.appengine.ext import ndb
from models import Slice, Block

class MemcacheKeeper():
    def write(self, entries):
        shard_string_index = SHARD_STRING_INDEX.format(random.randint(0, NUM_SHARDS - 1))
        slice = memcache.get(shard_string_index)
        if slice:
            entries.append(slice)
        memcache.set(shard_string_index, '\r\n'.join(entries))

    @ndb.transactional
    def read(self):
        contents=[]
        shard_string_indexes = ['simmetrica:{0}'.format(shard) for shard in range(0, NUM_SHARDS)]
        slices = memcache.get_multi(shard_string_indexes)
        contents.extend(slices.values())
        memcache.delete_multi(shard_string_indexes)
        content='\r\n'.join(contents)
        if WRITE_BLOCK:
            Block(content=contents).put()
        return content

class SliceKeeper():
    def write(self, entries):
        shard_string_index = str(random.randint(0, NUM_SHARDS - 1))
        slice = Slice.get_by_id(shard_string_index)
        if slice is None:
            slice = Slice(id=shard_string_index)
        if slice.content:
            entries.append(slice.content)
        slice.content = '\r\n'.join(entries)
        slice.put()

    @ndb.transactional
    def read(self):
        contents=[]
        for slice in Slice.query():
            contents.append(slice.content)
            slice.content=[]
            slice.put()
        content='\r\n'.join(contents)
        if WRITE_BLOCK:
            Block(content=contents)
        return content

Keeper={USE_MEMCACHE_KEEPER: MemcacheKeeper(), USE_SLICE_KEEPER: SliceKeeper()}[USE_MEMCACHE_KEEPER]

