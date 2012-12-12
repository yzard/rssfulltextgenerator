#!/usr/bin/python

import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class DownloadHandler(webapp2.RequestHandler):
	def get(self, resource):
		resource = str(urllib.unquote(resource))
		blob_info = blobstore.BlobInfo.get(resource)
		self.send_blob(blob_info)

app = webapp2.WSGIApplication([
	('/rss/([^/]+)?', DownloadHandler),
	] debug=True)
