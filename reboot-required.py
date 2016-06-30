#! /usr/bin/python
########################################################################
# Informs the users if there are updates that require a reboot.
# Copyright (C) 2016  Carl J Smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
from os.path import exists
from os import system
from os import listdir
from os import popen
from os import geteuid
if exists('/var/run/reboot-required'):
	#check for root since shortcuts need to be installed for all users
	if geteuid() != 0:
		print 'ERROR: this command must be ran as root!'
		print 'This will message all users on the system!'
		exit()
	else:
		# grab a list of users logged into the system
		loggedIn=popen('users').read()
		# if the users command executed successfully
		if loggedIn != -1:
			# strip the endline junk
			loggedIn=loggedIn.strip()
			# split the list based on spaces into an array
			loggedIn=loggedIn.split(' ')
			# remove duplicate entries in the list
			loggedIn=list(set(loggedIn))
		else:
			# the user check command failed
			exit()
		# array to store commands to be launched 
		restartPayload = []
		# compare logged in users to users home directory
		for user in listdir('/home'):
			# if user is logged into the system
			if user in loggedIn:
				# create a command to notify each user who is logged in using notify-send
				# send the output of this command to /dev/null in order to prevent garbage
				# output
				restartPayload.append("su -p "+user+' -c \'notify-send --urgency=critical --icon=reboot-notifier "Please reboot the system :D\nReboot required to finish installing updates!"\' > /dev/null')
		# for each item in the generated payload
		for item in restartPayload:
			# launch the command
			system(item)
