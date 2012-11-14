#!/usr/bin/python

import RssFullTextGenerator

from google.appengine.api import files
from google.appengine.ext import blobstore
from google.appengine.api import memcache

infos =[
{
	'func' : 'cnBeta',
	'url' : 'http://www.cnbeta.com/backend.php?atom'
	'num' : 60	
},
]

def generate_all():
	for site in infos:
		cache_key = '%s.cache' % (site['func'])
		rss_key = '%s.rss' % (site['func'])

		# generate feed object
		feed = RssFullTextGenerator(site['func'], site['url'], site['num'])
	
		# get cache from memcache if exists and load it
		cache = memcache.get(key=cache_key)
		feed.readFrom(cache)

		# generate rss feed
		rss = feed.generate()
	
		# get new cache and write it into memcache
		cache = StringIO.StringIO()
		feed.writeTo(cache)
		memcache.set(key=cache_key, value= cache, time=3600)

		# write rss file to memcache
		memcache.set(key=rss_key, value=rss, time=3600)

if __name__ == '__main__':
	generate_all()
