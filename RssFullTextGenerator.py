#!/usr/bin/python

import re
import datetime
import pickle
import StringIO

import feedparser
import feedgenerator
import httplib2
from bs4 import BeautifulSoup

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
		self.items = list()

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

	def writeToDisk(self, string):
		pickle.dump(self.items, fp)
		
	def readFromDisk(self, fp):
		import pickle
		try:
			self.items = pickle.load(fp)
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
		
		s = StringIO.StringIO()
		feed.write(s, 'utf-8')
		return s.getvalue()

	def _parseFeed(self):
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

	def generate(self):
		self._parseFeed()
		return self._generateRss()

if __name__ == '__main__':
	url = 'http://www.cnbeta.com/backend.php?atom'
	feed = RssFullTextGenerator('cnBeta', url, 60)
	fp = open('tmp.rss', 'wb')
	s = feed.generate()
	fp.write(s)
	fp.close()

