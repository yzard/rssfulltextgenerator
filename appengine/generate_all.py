#!/usr/bin/python

import webapp2
from google.appengine.api import memcache

from RssFullTextGenerator import RssFullTextGenerator
from Configure import Infos

class GenerateAll(webapp2.RequestHandler):
	def get(self):
		for site in Infos:
			func_name = site['func'].__name__
			cache_key = '%s.cache' % (func_name.lower())
			rss_key = '%s.xml' % (func_name.lower())

			# generate feed object
			feed = RssFullTextGenerator(site['func'], site['url'], site['num'])
	
			# get cache from memcache if exists and load it
			cache = memcache.get(key=cache_key)
			feed.setItems(cache)

			# generate rss feed
			rss = feed.generate()
		
			# get new cache and write it into memcache
			cache = feed.getItems()
			memcache.set(key=cache_key, value=cache, time=3600)

			# write rss file to memcache
			memcache.set(key=rss_key, value=rss, time=3600)
			
			self.response.write('Generated ' + str(len(feed.items)) + ' items')

app = webapp2.WSGIApplication([('/generate_all', GenerateAll)], debug=True)
