#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Matteo Fumi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


## CONFIGURATION ##
tipsdb = "" 			#Path of tips database (leave blank if it's in current directory)
				#Configure it if you've symlink this script!!!

colorcommand = "\033[93m"	#Color of command

version_tips = 4 		#NOT edit - ONLY for hacks!


import sys
import sqlite3
from urllib2 import urlopen


##
# Get arguments
##
try:
	argument = sys.argv[1]
except:
	print "	Usage: ./tips.py [TAG]"
	print "	--help for more informations"
	print "	--check for program and database updates from GitHub\n"
	sys.exit()

##
# Tips DB config
#
if tipsdb == "":
	tipsdb = "tips.sqlite"

## Connect to sqlite db
try:
	con = sqlite3.connect(tipsdb)
except:
	print "	Can't locate tips.sqlite in current directory!\n"
	sys.exit()


##
# Parse -- commands
##

## --help
if argument == "--help":
	print "	This tool helps you retrieve the most useful linux commands."
	print "	This script performs a search through tags in a database."
	print "	Usage: ./tips.py [TAG]"
	print "	If [TAG] is 'all', you can retrieve all database commands."
	sys.exit()

## --check
elif argument == "--check":
	try:
		# Script version check
		ur = urlopen("https://raw.github.com/merto/tips/master/version.cfg").read()
		if int(ur) > int(version_tips):
			print "New version of tips!! Get it on https://github.com/merto/tips"
		else:
			print "Your tips is updated!"

		# Script version check
		ur = urlopen("https://raw.github.com/merto/tips/master/version-db.cfg").read()

		cur = con.cursor()
		cur.execute('SELECT value FROM config WHERE key = "version_db";')
		version_db = cur.fetchone()[0]

		if int(ur) > int(version_db):
			print "New version of DB!! Get it on https://github.com/merto/tips"
		else:
			print "Your DB of tips is updated!"
	except:
		print "There was an error while retrieve information from GitHub. Internet connection is OK?"

	sys.exit()


print "Tag search: " + argument

try:
	#Search tag in db
	cur = con.cursor()

	#"all" tag
	if argument != "all":
		sqlwhere = ' WHERE tags LIKE "%' + argument + '%" OR command LIKE "%' + argument + '%"'
	else:
		sqlwhere = ''

	cur.execute('SELECT command,description FROM commands' + sqlwhere + ';')
	for row in cur:
	    print "	" + colorcommand + row[0] + "\033[0m" + "  >> " + row[1]
except:
	print "There was an error with database file. Have you configured me properly?"

#Close connection
con.close()
