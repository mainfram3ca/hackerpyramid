#!/usr/bin/env python
import os, sqlite3

videosdir = "../Audience/videos"
dbfile = "../Console/database.sqlite"

conn = sqlite3.connect(dbfile)
c = conn.cursor()

c.execute('drop table if exists videos')
c.execute('create table videos (used NUMERIC, filename TEXT)')


for (_, _, filenames) in os.walk(videosdir):
	continue


for f in filenames:
	if ".mp4" in f:
		print f
		c.execute('insert into videos (used,filename) values (0,?)',(f,))

conn.commit()


