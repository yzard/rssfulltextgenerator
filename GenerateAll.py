#!/usr/bin/python

import pickle

from RssFullTextGenerator import RssFullTextGenerator
from Configure import Infos, OUTPUT_XML_DIRECTORY, OUTPUT_CACHE_DIRECTORY

class GenerateAll():
	for site in Infos:
		func_name = site['func'].__name__
		cache_key = '%s.cache' % (func_name.lower())
		rss_key = '%s.xml' % (func_name.lower())

		# generate feed object
		feed = RssFullTextGenerator(site['func'], site['url'], site['num'])

		# get cache from memcache if exists and load it
		try:
			cache_file = open('/'.join(OUTPUT_CACHE_DIRECTORY, cache_key), 'rb')
			cache = pickle.load(cache_file)
		except:
			cache = None
		feed.setItems(cache)

		# generate rss feed
		rss = feed.generate()
	
		# get new cache and write it into memcache
		cache = feed.getItems()
		cache_file = open('/'.join(OUTPUT_CACHE_DIRECTORY, cache_key), 'wb')
		pickle.dump(cache, cache_file)
		cache_file.close()

		# write rss file to memcache
		xml_file = open('/'.join(OUTPUT_XML_DIRECTORY, rss_key), 'w')
		xml_file.write(rss)
		xml_file.close()

if __name__ == '__main__':
	GenerateAll()

