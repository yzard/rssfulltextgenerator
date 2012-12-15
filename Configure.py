#!/usr/bin/python

from BeautifulSoup import BeautifulSoup

# output directory
OUTPUT_XML_DIRECTORY='.'
OUTPUT_CACHE_DIRECTORY='.'

def cnBeta(raw):
	raw = raw.decode('gb18030').encode('utf-8')
	soup = BeautifulSoup(raw)

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


