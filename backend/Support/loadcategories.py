#! /usr/bin/python

import sys
import sqlite3

dbfile = "../Console/database.sqlite"

data = {}
data['records'] = []

title = ""
hint = ""
answers = []


fn = open(sys.argv[1],'r')
for l in fn:
	if l == '\n':
		r = dict(Title=title,Hint=hint,Answers=','.join(answers))
		data['records'].append(r)
		title = ""
		hint = ""
		answers = []
	elif title == "":
		title = l.strip('\n')
	elif hint == "":
		hint = l.strip('\n')
	else:
		answers.append(l.strip('\n'))

conn = sqlite3.connect(dbfile)
c = conn.cursor()

#CREATE TABLE catagories (preselect NUMERIC, used NUMERIC, Answers TEXT, Hint TEXT, Title TEXT, id INTEGER PRIMARY KEY);

c.execute('drop table if exists catagories')
c.execute('create table catagories (preselect NUMERIC DEFAULT 0, used NUMERIC DEFAULT 0, Answers TEXT, Hint TEXT, Title TEXT, id INTEGER PRIMARY KEY)')



for r in data['records']:
	c.execute('insert into catagories (Answers,Hint,Title) values (?,?,?)',(r['Answers'],r['Hint'],r['Title']))

conn.commit()




