#!/usr/bin/python

import urllib
import webapp2
from google.appengine.api import memcache

class DownloadHandler(webapp2.RequestHandler):
	def get(self, resource):
		resource = str(urllib.unquote(resource)).lower()
		data = memcache.get(resource)	
		self.response.headers['Content-Type'] = 'text/plain'
		if data:
			self.response.out.write(data)
		else:
			self.response.out.write(resource + ' is not ready yet!')

app = webapp2.WSGIApplication([
	('/rss/([^/]+)?', DownloadHandler),
	], debug=True)
