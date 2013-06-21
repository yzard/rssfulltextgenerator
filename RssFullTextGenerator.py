#!/usr/bin/python

import re
import datetime
import StringIO

import feedparser
import feedgenerator
import httplib2

import Encoding

class RssFullTextGenerator:
	def __init__(self, func, url, number):
		# link : content 
		self.func = func 
		self.func_name = func.__name__
		self.url = url
		self.number = number
		self.items = list()

	def _find(self, link):
		for item in self.items:
			l = item['title']
			if link == l:
				return item['description']
		return None

	def _getContent(self, func, link):
		try:
			h = httplib2.Http()
			response, content = h.request(link, 'GET',)
			return self.func(content)
		except KeyboardInterrupt:
			raise KeyboardInterrupt

	def setItems(self, items):
		if items != None:
			self.items = items

	def getItems(self):
		return self.items

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
		num = 0
		for i in newItems:
			num += 1
			print "Processing page (" + str(num) + "): " + i['link']
			if self._find(i['title']):
				continue
			
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

