#!/usr/bin/python

from Configure import *
from RssFullTextGenerator import RssFullTextGenerator

def main():
	feed = RssFullTextGenerator(cnBeta, 'http://www.cnbeta.com/backend.php?atom', 60)
	
	feed.setItems(None)
	rss = feed.generate()

	f = open('tmp.rss', 'wb')
	f.write(rss)
	f.close()

if __name__ == '__main__':
	main()
