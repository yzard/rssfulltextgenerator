#!/usr/bin/python

import re
import datetime

import feedparser
import feedgenerator
import httplib2
from bs4 import BeautifulSoup

[
{
	'func' : 'cnBeta',
	'url' : 'http://www.cnbeta.com/backend.php?atom'
}
]

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

class RssFullTextGenerator:
	def __init__(self, func_name, url, number):
		# link : content 
		self.func_name = func_name
		self.func = globals()[func_name] 
		self.url = url
		self.number = number

	def _find(self, link):
		for item in self.items:
			l = item['title']
			if link == l:
				return True
		return False

	def _getContent(self, func, link):
		try:
			h = httplib2.Http()
			response, content = h.request(link, 'GET',)
			return self.func(content)
		except:
			print 'Error when opening link:', link
			return None

	def _writeToDisk(self):
		import pickle
		f = open(self.func_name, 'wb')
		pickle.dump(self.items, f)
		f.close()
		
	def _readFromDisk(self):
		import pickle
		try:
			f = open(self.func_name, 'rb')
			self.items = pickle.load(f)
			f.close()
		except:
			self.items = list()

	def _generateRss(self):
		# generate new xml file
		# make a copy and unzip and reverse
		allItems = self.items[:]
		allItems.reverse()

		feed = feedgenerator.Rss201rev2Feed(
			title = self.func_name + ' full text feed',
			link = self.url,
			feed_url = u'test.org/rss',
			description = u'Full text RSS feed for ' + self.func_name,
			language = u'zh',
		)

		for item in allItems:
			feed.add_item(
				title = item['title'],
				link = item['link'],
				description = item['description'],
			)
		
		fp = open(self.func_name + '_full_text.rss', 'w')
		feed.write(fp, 'utf-8')
		fp.close()

	def _parseFeed(self):
		# read self.items
		self._readFromDisk()

		feed = feedparser.parse(self.url)
		newItems = feed['items']
		newItems.reverse()

		# process from the oldest to newest
		print 'Total number of pages: ', len(newItems)
		for i in newItems:
			if self._find(i['title']):
				print '- skipping: ', i['title']
				continue
			
			print '- processing: ', i['title']

			# get full text content
			content = None
			while not content:
				content = self._getContent(self.func, i['link'])

			self.items.append({
				'title' : i['title'],
				'link'	: i['link'],
				'description' : content,
				'pubDate' : i['published'],
			})

			# drop old one
			if len(self.items) > self.number:
				self.items.pop(0)

		# write self.items
		self._writeToDisk()
		
	def generate(self):
		self._parseFeed()
		self._generateRss()

if __name__ == '__main__':
	url = 'http://www.cnbeta.com/backend.php?atom'
	feed = RssFullTextGenerator('cnBeta', url, 60)
	feed.generate()

