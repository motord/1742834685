__author__ = 'peter'

NUM_SHARDS = 16
SHARD_STRING_INDEX = 'simmetrica:{0}'
WRITE_BLOCK = False
USE_MEMCACHE_KEEPER = 1
USE_SLICE_KEEPER = 2
CACHE_TIMEOUT=12 * 60
CACHE_KEY='simmetrica:sql:{0}'

# BigQuery API Settings
SCOPE = 'https://www.googleapis.com/auth/bigquery'
PROJECT_ID = 'samdeha.com:qrcache'


