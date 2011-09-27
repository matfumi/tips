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
tipsdb = "" 			#Path of tips database (leave blank if in current directory)
colorcommand = "\033[93m"	#Color of command


import sys
import sqlite3

#Get arguments
try:
	argument = sys.argv[1]
except:
	print "	Usage: ./tips.py [TAG]"
	print "	--help for more informations\n"
	sys.exit()

#Only --help command
if argument == "--help":
	print "	This tool helps you retrieve the most useful linux commands."
	print "	This script performs a search through tags in a database."
	print "	Usage: ./tips.py [TAG]"
	print "	If [TAG] is 'all', you can retrieve all database commands."
	sys.exit()


#Tips DB config
if tipsdb == "":
	tipsdb = "tips.sqlite"

#Connect to sqlite db
try:
	con = sqlite3.connect(tipsdb)
except:
	print "	Can't locate tips.sqlite in current directory!\n"
	sys.exit()


print "Tag search: " + argument

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

#Close connection
con.close()
