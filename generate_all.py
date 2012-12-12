#!/usr/bin/python

import RssFullTextGenerator

from google.appengine.api import files
from google.appengine.ext import blobstore

infos =[
{
	'func' : 'cnBeta',
	'url' : 'http://www.cnbeta.com/backend.php?atom'
	'num' : 60	
}
]


def generate_all.py():
	for site in infos:
		feed = RssFullTextGenerator(site['func'], site['url'], site['num'])
		feed.generate()

