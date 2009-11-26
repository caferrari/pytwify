import pynotify, twitter, os.path, os, sys
import urllib2
from time import sleep

import ConfigParser

config = ConfigParser.ConfigParser()

if pynotify.init("Twitter"):

	configFile = os.getenv("HOME")+'/.pytwify.cfg'
	cachePath = '/tmp/pytwify/'
	lastId = 0
	
	while True:

		config.read(configFile)			
		username = config.get('auth', 'username')
		password = config.get('auth', 'password')
		
		lastIdFile = cachePath + username+".last"

		api = twitter.Api(username, password)

		if not os.path.exists(lastIdFile):
			if not os.path.exists(cachePath):
				os.mkdir(cachePath)
					
			try:		
				twitts = api.GetFriendsTimeline(count = 1)
				if len(twitts) > 0:
					lastId = twitts[0].id
					if lastId != 0:
						open(lastIdFile,"wb").write(str(lastId))
				
			except:
				print "auth error =("
				pynotify.Notification("PyTwiFy: Error ", "Couldn't authenticate.\n Edit the file "+configFile).show()
									
		else:
		
			lastId = open(lastIdFile).read()
	
			try:

				print "lastId is: " + str(lastId)
	
				twitts = api.GetFriendsTimeline(since_id = lastId)

				print "twitt(s) retrieved: " + str(len(twitts))

				if len(twitts) > 0:
					lastId = twitts[0].id

					for i in range(len(twitts)-1, -1, -1):
						t = twitts[i]
						print "showing twitt from " + t.user.screen_name + " (id:" + str(t.id) + ")"
					
						uri = cachePath + "image_" + t.user.screen_name 
						if not os.path.exists(uri):
							open(uri,"w").write(urllib2.urlopen(t.user.profile_image_url).read())
					
						n = pynotify.Notification("PyTwiFy: " + t.user.screen_name, t.text, uri)
						n.show()
					
					open(lastIdFile,"wb").write(str(lastId))
						
			except:
				print "some error =("
				pynotify.Notification("PyTwiFy: Error ", "Twitter is \"baleiando\".").show()
						
		print "next lastId is: " + str(lastId)
		print "sleeping..."

		sleep(60)
		
