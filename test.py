#!/usr/bin/python

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

def main():
	feed = RssFullTextGenerator(cnBeta, 'http://www.cnbeta.com/backend.php?atom', 60)
	
	feed.setItems(None)
	rss = feed.generate()

	f = open('tmp.rss', 'wb')
	f.write(rss)
	f.close()

