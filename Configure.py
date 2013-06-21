#!/usr/bin/python

from bs4 import BeautifulSoup
import Encoding 

# output directory
OUTPUT_XML_DIRECTORY='/var/www/html/rss'
OUTPUT_CACHE_DIRECTORY='/home/zyin/rss_cache'

def cnBeta(raw):
	# decode and encoding
	newRaw = Encoding.try_decode(raw)
	if not newRaw:
		print 'Try decoding failed'
		return 'N/A'

	newRaw = Encoding.encode_ignore(newRaw, 'utf-8')

	soup = BeautifulSoup(raw)
	content = soup.find('div' , { 'class' : 'content'})

	if not content:
		return 'N/A'

	return str(content).replace('\n', '').replace('\r', '')

# parameters 
Infos =[
{
	'func' : cnBeta,
	'url' : 'http://www.cnbeta.com/backend.php?atom',
	'num' : 60,
},
]


