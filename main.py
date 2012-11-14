#!/usr/bin/python

import webapp2
from google.appengine.api import memcache

class DownloadHandler(webapp2.RequestHandler):
	def get(self, resource):
		resource = str(urllib.unquote(resource))
		data = memcache.get(resource)	
		self.response.out.write(data)

app = webapp2.WSGIApplication([
	('/rss/([^/]+)?', DownloadHandler),
	] debug=True)
