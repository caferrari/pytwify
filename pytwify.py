import pynotify, twitter, os.path, os, sys
from time import sleep

import ConfigParser

config = ConfigParser.ConfigParser()

if pynotify.init("Twitter"):

	firstRun = True
	
	while True:
	
			config.read(os.getenv("HOME")+'/.pytwify.cfg')
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
					pynotify.Notification("Pytter: Error ", "Couldn't authenticate.\n Edit the file pytter.cfg").show()
							
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
					pynotify.Notification("Pytter: Error ", "Some connection error ocurred...").show()
					
			config.set("vars","lastId",lastId)
			config.write(open(os.getenv("HOME")+'/.pytwify.cfg','wb'))
		
			print "next lastId is: " + str(lastId)
			print "sleeping..."

			sleep(60)
		
		
