#!/usr/bin/python

import BeautifulSoup
import Encoding 

# output directory
OUTPUT_XML_DIRECTORY='.'
OUTPUT_CACHE_DIRECTORY='.'

def cnBeta(raw):
	# decode and encoding
	raw = Encoding.decode_ignore(raw, 'gb18030')
	raw = Encoding.encode_ignore(raw, 'utf-8')

	soup = BeautifulSoup.BeautifulSoup(raw)
	content = soup.find(id='news_content')
		
	if not content:
		return 'N/A'

	# clean
	result = str(content).replace('\n', '').replace('\r', '')
	return result

# parameters 
Infos =[
{
	'func' : cnBeta,
	'url' : 'http://www.cnbeta.com/backend.php?atom',
	'num' : 60,
},
]


