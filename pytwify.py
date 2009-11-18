import pynotify, twitter, os.path, os, sys
from time import sleep

import ConfigParser

config = ConfigParser.ConfigParser()

if pynotify.init("Twitter"):

	firstRun = True
	configFile = os.getenv("HOME")+'/.pytwify.cfg'
	
	while True:

			try:
				
				config.read(configFile)			
				username = config.get('auth', 'username')
				password = config.get('auth', 'password')
				lastId = config.getint('vars', 'lastId')
		
				api = twitter.Api(username, password)

				if firstRun:
							
					try:
						twitts = api.GetFriendsTimeline(count = 1)
						firstRun = False
						if len(twitts) > 0:
							lastId = twitts[0].id
				
					except:
						print "auth error =("
						pynotify.Notification("PyTwiFy: Error ", "Couldn't authenticate.\n Edit the file "+configFile).show()
									
				else:

					try:

						print "lastId is: " + str(lastId)
				
						twitts = api.GetFriendsTimeline(since_id = lastId)

						print "twitt(s) retrieved: " + str(len(twitts))
		
						if len(twitts) > 0:
							lastId = twitts[0].id

							for i in range(len(twitts)-1, -1, -1):
								t = twitts[i]
								print "showing twitt from " + t.user.screen_name + " (id:" + str(t.id) + ")"
								pynotify.Notification("Pytter: " + t.user.screen_name, t.text).show()
				
					except:
						print "some error =("
						pynotify.Notification("PyTwiFy: Error ", "Some connection error ocurred...").show()
					
				config.set("vars","lastId",lastId)
				config.write(open(configFile,'wb'))
		
				print "next lastId is: " + str(lastId)
				print "sleeping..."
				
			except:
				pynotify.Notification("PyTwiFy: Error ", "Error while reading the configuration.\n Please setup the file "+configFile).show()

			sleep(60)
		
		
