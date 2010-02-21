#!/usr/bin/python2.6
# -*- coding: utf-8 -*-#
import pynotify, twitter, os.path, os, sys, urllib2, tempfile, commands
from time import sleep
from ConfigParser import ConfigParser

class pytwify:

	def log(self, msg):
		print msg

	def saveConf(self):
		self.log ('Saving the configfile %s' % self.configFile)
		self.config.has_section('config') or self.config.add_section('config')
		self.config.set('config', 'auth.username', self.username)
		self.config.set('config', 'auth.password', self.password)
		self.config.set('config', 'lastId', self.lastId)
		
		for d in ('%s/.pytwify' % self.homedir, '%s/.pytwify/cache' % self.homedir):
			os.path.isdir(d) or os.mkdir(d)
				
		self.config.write(open(self.configFile, 'wb'))
				
		if self.username == 'not-set':
			self.log ('Put your login info in the config file\n\nbye bye...')
			sys.exit(0) # Maybe a screen to enter the username and password? mayyyybe
		
	def readConf(self):
		self.config = ConfigParser()
		if os.path.isfile(self.configFile):
			self.config.read(self.configFile)
			self.username = self.config.get('config', 'auth.username')
			self.password = self.config.get('config', 'auth.password')
			self.lastId = self.config.get('config', 'lastId')
			
		if self.username == 'not-set':
			self.saveConf()
			
	def __init__(self):
		self.username = 'not-set'
		self.password = 'not-set'
		self.lastId = 0
		self.homedir = os.path.expanduser("~")
		self.configFile = self.homedir + '/.pytwify/config.cfg'
		self.cachePath =  self.homedir + '/.pytwify/cache/'
		self.readConf()
		self.twitter = twitter.Api(self.username, self.password)
		pynotify.init('pytwify')
		self.showtime()
		
	def showtime(self):
		if commands.getoutput('purple-remote getstatus') == 'away':
			self.log ('Hello? are you there?..')
			sleep(10)
		else:
			try:
				twitts = self.twitter.GetFriendsTimeline(since_id = int(self.lastId))
				self.log ('%d new tweets found' % len(twitts))
				if (twitts):
					self.lastId = twitts[0].id
		 			self.saveConf()
				while twitts:
					t = twitts.pop()
					uri = '%s/image_%s' % (self.cachePath, t.user.screen_name)
					os.path.isfile(uri) or open(uri, 'w').write(urllib2.urlopen(t.user.profile_image_url).read())
					pynotify.Notification('PyTwiFy: %s ' % t.user.screen_name, t.text, uri).show()
			except:
				self.log('Some error trying to retrive the tweets')
			
			self.log ('sleeping...')
			sleep(60)
			
		self.showtime()
		
pytwify()
