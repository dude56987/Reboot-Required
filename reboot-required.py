#! /usr/bin/python
########################################################################
# Informs the users if there are updates that require a reboot.
# Copyright (C) 2014  Carl J Smith
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
		restartPayload = []
		for user in listdir('/home'):
				if popen('ps -u '+user+' | grep init').read().find('init') != -1:
					# create a command to notify each user who is logged in
					restartPayload.append("su "+user+' bash -c \'notify-send --urgency=critical --icon=reboot-notifier "Please reboot the system :D\nReboot required to finish installing updates!"\'')
		for item in restartPayload:
			# launch each of the commands created previously
			system(item)
