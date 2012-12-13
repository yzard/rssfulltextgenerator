#!/usr/bin/python

import webapp2
from google.appengine.api import memcache

from RssFullTextGenerator import RssFullTextGenerator
from BeautifulSoup import BeautifulSoup

def cnBeta(raw):
	raw = raw.decode('gb18030').encode('utf-8')
	soup = BeautifulSoup(raw)

	content = soup.find(id='news_content')
		
	if not content:
		return 'N/A'

	# clean
	#[x.extract() for x in content.find_all('script')]
	result = str(content).replace('\n', '').replace('\r', '')

	return result

infos =[
{
	'func' : cnBeta,
	'url' : 'http://www.cnbeta.com/backend.php?atom',
	'num' : 60,
},
]


class GenerateAll(webapp2.RequestHandler):
	def get(self):
		for site in infos:
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
