#! /usr/bin/python

import socket
import web
import subprocess
import os
import time
import math
import json
import buzz
import random
import signal
import threading
import sys
import pygame

#
# Management
#

# uri: /manage
#
# show the management interface
# uses the "theform" template

class management:
	def GET(self):
		# turn off the bottom status bar
		#uzbl_cmd('set show_status = 0')
		web.header("Cache-Control", "no-cache, max-age=0,no-store")
	
		# this is just a placeholder so that I don't foget how to add dynamic form elements
		# multiple submit buttons dont seem to act as I expected, they *all* have value.
		# is this new bahaviour?
		#theform = web.form.Form(web.form.Button('START',value="START"),web.form.Button('STOP',value="STOP"))
		#f = theform()

		# generate team list with selector
		team_l = []

		db_teamscores = web.database(dbn='sqlite',db="%s/%s"%(BASE,"teamscores.sqlite"))
		rs = db_teamscores.query("select id as id,name as name,score as score from teamscores order by score DESC;")
		for r in rs:
			team_l.append(r)

		# create the database
		if not os.path.isfile("%s/%s"%(BASE,"categories.sqlite")):
			return "There is no CATEGORIES DATABASE\n"

		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))

		# generate the list of categories
		rs = db.query('select id as id, category as category, hint as hint,used as used from categories order by used,category')

		cats_l = []
		for r in rs:
			cats_l.append(r)

		#get the management template
		render = web.template.render(STATIC)
		return render.manage(ACTIVECATEGORY,ACTIVETEAM,team_l,cats_l)


class editor:
	def GET(self):
		#teamscores
		#id,team,score
		if not os.path.isfile("%s/%s"%(BASE,"teamscores.sqlite")):
			db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"teamscores.sqlite"))
			db.query('create table teamscores(id INTEGER PRIMARY KEY, name char(40), score INT);')

		db_teamscores = web.database(dbn='sqlite',db="%s/%s"%(BASE,"teamscores.sqlite"))
		rs = db_teamscores.query("select id as id,name as name,score as score from teamscores;")

		team_l = []
		for r in rs:
			team_l.append(r)

		#categories
		#id,category,hint,a1,a2,a3,a4,a5,a6,a7,teamid,used
		if not os.path.isfile("%s/%s"%(BASE,"categories.sqlite")):
			db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))
			db.query('create table categories(id INTEGER PRIMARY KEY, category char(40), hint char(100),a1 char(40), a2 char(40), a3 char(40), a4 char(40), a5 char(40), a6 char(40), a7 char(40), teamid INT DEFAULT 0, used char(1), ord INT DEFAULT 0);')

		db_categories = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))
		rs = db_categories.query("select id as id, category as category, hint as hint, a1 as a1, a2 as a2, a3 as a3, a4 as a4, a5 as a5, a6 as a6, a7 as a7,teamid as teamid,used as used from categories;")

		category_l = []
		for r in rs:
			category_l.append(r)

		#get the management template
		render = web.template.render(STATIC)
		return render.editor(team_l,category_l)

class team_add:
	def GET(self):
		namelength = web.form.regexp(r".{3,40}$",'must be between 3 and 20 characters')
		f = web.form.Form(
			web.form.Textbox("TeamName", namelength, description="Team Name"),
			web.form.Button("submit", type="submit",description="submit")
		)
		r = f()
		render = web.template.render(STATIC)
		return render.team_add(r)

	def POST(self):
		namelength = web.form.regexp(r".{3,40}$",'must be between 3 and 20 characters')
		f = web.form.Form(
			web.form.Textbox("TeamName", namelength, description="Team Name"),
			web.form.Button("submit", type="submit",description="submit")
		)
		r = f()
		if not f.validates():
			render = web.template.render(STATIC)
			return render.team_add(r)
		else:
			data = web.input()
			db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"teamscores.sqlite"))
			db.query('insert into teamscores (name,score) values (%s,0)'%(web.db.sqlquote(data.TeamName)))
			render = web.template.render(STATIC)
			#return render.team_add(r)
			return web.seeother("/editor")

class team_edit:
	def GET(self,tid):
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"teamscores.sqlite"))
		rs = db.query('select name as name from teamscores where id = "%s"'%(tid))

		for r in rs:
			name = r.name

		namelength = web.form.regexp(r".{3,40}$",'must be between 3 and 20 characters')
		f = web.form.Form(
			web.form.Hidden("id", description="id",value=tid),
			web.form.Textbox("TeamName", namelength, description="Team Name",value=name),
			web.form.Button("submit", type="submit",description="submit")
		)

		r = f()
		render = web.template.render(STATIC)
		return render.team_edit(r)

	def POST(self,tid):
		namelength = web.form.regexp(r".{3,40}$",'must be between 3 and 20 characters')
		f = web.form.Form(
			web.form.Hidden("id", description="id",value=tid),
			web.form.Textbox("TeamName", namelength, description="Team Name"),
			web.form.Button("submit", type="submit",description="submit")
		)
		r = f()
		if not f.validates():
			render = web.template.render(STATIC)
			return render.team_add(r)
		else:
			data = web.input()
			db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"teamscores.sqlite"))
			db.query('update teamscores set name = %s where id = %s'%(web.db.sqlquote(data.TeamName),web.db.sqlquote(data.id)))
			render = web.template.render(STATIC)
			#return render.team_add(r)
			return web.seeother("/editor")

class team_delete:
	def GET(self,tid):
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"teamscores.sqlite"))
		db.query('delete from teamscores where id = %s'%(web.db.sqlquote(tid)))
		return web.seeother("/editor")

class category_edit:
	def GET(self,cid):
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))
		rs = db.query('select category as category,hint as hint, a1 as a1, a2 as a2, a3 as a3, a4 as a4, a5 as a5, a6 as a6, a7 as a7, used as used, teamid as teamid from categories where id = %s'%(web.db.sqlquote(cid)))

		for r in rs:
			category = r.category
			hint = r.hint
			a1 = r.a1
			a2 = r.a2
			a3 = r.a3
			a4 = r.a4
			a5 = r.a5
			a6 = r.a6
			a7 = r.a7
			used = r.used
			affinity = r.teamid

		categorylength = web.form.regexp(r".{3,40}$",'must be between 3 and 40 characters')
		hintlength = web.form.regexp(r".{3,100}$",'must be between 3 and 100 characters')
		alength = web.form.regexp(r".{1,40}$",'must be between 1 and 40 characters')
		f = web.form.Form(
			web.form.Hidden("id",value=cid),
			web.form.Textbox("category", categorylength, description="Category",value=category),
			web.form.Textbox("hint", hintlength, description="Hint",value=hint),
			web.form.Textbox("a1", alength, description="Answer 1",value=a1),
			web.form.Textbox("a2", alength, description="Answer 2",value=a2),
			web.form.Textbox("a3", alength, description="Answer 3",value=a3),
			web.form.Textbox("a4", alength, description="Answer 4",value=a4),
			web.form.Textbox("a5", alength, description="Answer 5",value=a5),
			web.form.Textbox("a6", alength, description="Answer 6",value=a6),
			web.form.Textbox("a7", alength, description="Answer 7",value=a7),
			web.form.Textbox("teamid", description="Affinity", value=affinity),
			web.form.Textbox("used", description="Used", value=used),
			web.form.Button("submit", type="submit",description="submit")
		)
		r = f()
		render = web.template.render(STATIC)
		return render.category_edit(r)

	def POST(self,cid):
		categorylength = web.form.regexp(r".{3,40}$",'must be between 3 and 40 characters')
		hintlength = web.form.regexp(r".{3,100}$",'must be between 3 and 100 characters')
		alength = web.form.regexp(r".{1,40}$",'must be between 1 and 40 characters')
		f = web.form.Form(
			web.form.Hidden("id",value=cid),
			web.form.Textbox("category", categorylength, description="Category"),
			web.form.Textbox("hint", hintlength, description="Hint"),
			web.form.Textbox("a1", alength, description="Answer 1"),
			web.form.Textbox("a2", alength, description="Answer 2"),
			web.form.Textbox("a3", alength, description="Answer 3"),
			web.form.Textbox("a4", alength, description="Answer 4"),
			web.form.Textbox("a5", alength, description="Answer 5"),
			web.form.Textbox("a6", alength, description="Answer 6"),
			web.form.Textbox("a7", alength, description="Answer 7"),
			web.form.Textbox("teamid", description="Affinity"),
			web.form.Textbox("used", description="Used"),
			web.form.Button("submit", type="submit",description="submit")
		)
		r = f()
		if not f.validates():
			render = web.template.render(STATIC)
			return render.team_add(r)
		else:
			data = web.input()
			db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))
			db.query('update categories set category=%s, hint=%s, a1=%s, a2=%s, a3=%s, a4=%s, a5=%s, a6=%s, a7=%s, teamid=%s, used=%s where id = %s'%( web.db.sqlquote(data.category), web.db.sqlquote(data.hint), web.db.sqlquote(data.a1), web.db.sqlquote(data.a2), web.db.sqlquote(data.a3), web.db.sqlquote(data.a4), web.db.sqlquote(data.a5), web.db.sqlquote(data.a6), web.db.sqlquote(data.a7), web.db.sqlquote(data.teamid), web.db.sqlquote(data.used), web.db.sqlquote(data.id)))
			render = web.template.render(STATIC)
			return web.seeother("/editor")

class category_delete:
	def GET(self,cid):
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))
		db.query('delete from categories where id = %s'%(web.db.sqlquote(cid)))
		return web.seeother("/editor")

class category_add:
	def GET(self):
		categorylength = web.form.regexp(r".{3,40}$",'must be between 3 and 40 characters')
		hintlength = web.form.regexp(r".{3,100}$",'must be between 3 and 100 characters')
		alength = web.form.regexp(r".{1,40}$",'must be between 1 and 40 characters')
		f = web.form.Form(
			web.form.Textbox("category", categorylength, description="Category"),
			web.form.Textbox("hint", hintlength, description="Hint"),
			web.form.Textbox("a1", alength, description="Answer 1"),
			web.form.Textbox("a2", alength, description="Answer 2"),
			web.form.Textbox("a3", alength, description="Answer 3"),
			web.form.Textbox("a4", alength, description="Answer 4"),
			web.form.Textbox("a5", alength, description="Answer 5"),
			web.form.Textbox("a6", alength, description="Answer 6"),
			web.form.Textbox("a7", alength, description="Answer 7"),
			web.form.Textbox("teamid", description="Affinity", value="0"),
			web.form.Textbox("used", description="Used", value="N"),
			web.form.Button("submit", type="submit",description="submit")
		)
		r = f()
		render = web.template.render(STATIC)
		return render.category_add(r)

	def POST(self):
		categorylength = web.form.regexp(r".{3,40}$",'must be between 3 and 40 characters')
		hintlength = web.form.regexp(r".{3,100}$",'must be between 3 and 100 characters')
		alength = web.form.regexp(r".{1,40}$",'must be between 1 and 4 characters')
		f = web.form.Form(
			web.form.Textbox("category", categorylength, description="Category"),
			web.form.Textbox("hint", hintlength, description="Hint"),
			web.form.Textbox("a1", alength, description="Answer 1"),
			web.form.Textbox("a2", alength, description="Answer 2"),
			web.form.Textbox("a3", alength, description="Answer 3"),
			web.form.Textbox("a4", alength, description="Answer 4"),
			web.form.Textbox("a5", alength, description="Answer 5"),
			web.form.Textbox("a6", alength, description="Answer 6"),
			web.form.Textbox("a7", alength, description="Answer 7"),
			web.form.Textbox("teamid", description="Affinity"),
			web.form.Textbox("used", description="Used"),
			web.form.Button("submit", type="submit",description="submit")
		)
		r = f()
		if not f.validates():
			print "valid: %s"%f.validates()
			render = web.template.render(STATIC)
			return render.category_add(r)
		else:
			data = web.input()
			db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))
			db.query('insert into categories (category,hint,a1,a2,a3,a4,a5,a6,a7,teamid,used) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'%(web.db.sqlquote(data.category),web.db.sqlquote(data.hint),web.db.sqlquote(data.a1),web.db.sqlquote(data.a2),web.db.sqlquote(data.a3),web.db.sqlquote(data.a4),web.db.sqlquote(data.a5),web.db.sqlquote(data.a6),web.db.sqlquote(data.a7),web.db.sqlquote(data.teamid),web.db.sqlquote(data.used)))
			render = web.template.render(STATIC)
			#return render.team_add(r)
			return web.seeother("/editor")

class affinity_inc:
	def GET(self,cid):
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))
		db.query('update categories set teamid = teamid + 1 where id = "%s"'%(cid))
		return web.seeother("/editor")

class affinity_dec:
	def GET(self,cid):
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))
		db.query('update categories set teamid = teamid - 1 where id = "%s"'%(cid))
		return web.seeother("/editor")
		

###
### Podium
###

class hints:
	def GET(self):
		#print "HINTS: %s"%json.dumps(CAT_HINTS)

		render = web.template.render(STATIC)
		return render.hints(ACTIVETEAM,ACTIVESCORE,ACTIVECATEGORY,CAT_HINTS)


###
### hotlinks to functions.
###

# uri: /load_crash
# tell uzbl to start playing commercials
class load_crash:
	def GET(self):
		#uzbl_cmd('set uri = http://localhost:8080/commercial')
		uzbl_cmd('set uri = http://localhost:8080/crash')
		STOPCOMMERCIALS = False
		raise web.seeother('/manage')

# uri: /load_commercials
# tell uzbl to start playing commercials
class load_commercials:
	def GET(self):
		#uzbl_cmd('set uri = http://localhost:8080/commercial')
		uzbl_cmd('set uri = http://localhost:8080/bumper')
		STOPCOMMERCIALS = False
		raise web.seeother('/manage')

# uri: /load_showcategories
# tell uzbl to load the category selection page
# unless there is no active team set
class load_showcategories:
	def GET(self):
		if ACTIVETEAM != "":
			uzbl_cmd('set uri = http://localhost:8080/show_categories')
		else:
			print("NO ACTIVE TEAM. REFUSING TO SHOW CATEGORIES")
		raise web.seeother('/manage')

# uri: /load_attract
# tell uzbl to load the fancy logo page which will also play the theme
# the thema playback is built into the tempalte
class load_attract:
	def GET(self):
		uzbl_cmd('set uri = http://localhost:8080/attract')
		uzbl_cmd('set show_status = 0')
		raise web.seeother('/manage')

# uri: /load_silent
# tell uszle to load the simple logo page
class load_silent:
	def GET(self):
		uzbl_cmd('set uri = http://localhost:8080/silent')
		uzbl_cmd('set show_status = 0')
		raise web.seeother('/manage')

# uri: /load_playgame
# this will tell uzble to start a round with the 
# preset TEAM and CATEGORY
class load_playgame:
	def GET(self):
		time.sleep(.5)
		uzbl_cmd("js document.getElementById('teamname').innerHTML='%s'"%web.websafe(ACTIVETEAM))
		uzbl_cmd("js document.getElementById('teamscore').innerHTML='Score: %s'"%web.websafe(ACTIVESCORE))
		print("ACTIVETEAM = |%s|"%ACTIVETEAM)
		p = playthegame()
		t = threading.Timer(30, interrupt_thread, [p])
		t.start() 
		p.start()
		raise web.seeother('/manage')

# uri: /stop_commercials
# set the STOPCOMMERCIALS flag to true
# the commercials uri will stop gracefully at the end of the current commercial
class stop_commercials:
	def GET(self):
		global STOPCOMMERCIALS
		STOPCOMMERCIALS = True
		raise web.seeother('/manage')

# uri: /load_scores
# tell uzble to load the score page
class load_scores:
	def GET(self):
		uzbl_cmd('set uri = http://localhost:8080/show_scores')
		raise web.seeother('/manage')

# uri: /set_team/(.*)
# set the current team to whatever ID is indicated by the (.*)
# load the score as well
class set_team:
	def GET(self,teamid):
		global ACTIVETEAM
		global ACTIVETEAMID
		global ACTIVESCORE
		global ACTIVECATEGORY
		ACTIVECATEGORY = ""
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"teamscores.sqlite"))
		rs = db.query('SELECT name as name,score as score FROM teamscores WHERE id = "%s" ORDER BY RANDOM() LIMIT 1;'%teamid)
		for r in rs:
			ACTIVETEAM  = r.name
			ACTIVESCORE = r.score

		ACTIVETEAMID = teamid
		uzbl_cmd("set uri=http://localhost:8080/show_categories")
		raise web.seeother('/manage')

# uri: /inc_score/(.*)
# increment the teams score where the id = (.*)
class inc_score:
	def GET(self,teamid):
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"teamscores.sqlite"))
		rs = db.query('update teamscores set score = score+1 where id = %s'%teamid)
		raise web.seeother('/manage')

# uri: /dec_score/(.*)
# decrement the teams score where the id = (.*)
class dec_score:
	def GET(self,teamid):
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"teamscores.sqlite"))
		rs = db.query('update teamscores set score = score-1 where id = %s'%teamid)
		raise web.seeother('/manage')

# uri: /set_unused/(.*)
# set the category to "used" where the id = (.*)
class set_used:
	def GET(self,categoryid):
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))
		rs = db.query('update categories set used = "Y" where id = %s'%categoryid)
		raise web.seeother('/manage')

# uri: /set_unused/(.*)
# set the category to "unused" where the id = (.*)
class set_unused:
	def GET(self,categoryid):
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))
		rs = db.query('update categories set used = "N" where id = %s'%categoryid)
		raise web.seeother('/manage')

# uri: /reset_categories
# set all categories number the "order"
class reset_categories:
	def GET(self):
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))
		rs = db.query('SELECT id as id FROM categories')
		c = 0
		for r in rs:
			db.query('UPDATE categories set ord = %s where id = %s'%(c,r.id))
			c = c + 1
		
		raise web.seeother('/manage')


# uri: /reset_commercials
# set all commercials to unseen in the database
class reset_commercials:
	def GET(self):
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"commercials.sqlite"))
		rs = db.query('update commercials set seen = "N"')
		raise web.seeother('/manage')


# uri: /set_category/(.*)
# set the current category to whatever ID is indicated by the (.*)
# load the answers as well
class set_category:
	def GET(self,categoryid):
		global ACTIVECATEGORY
		global ACTIVEA1
		global ACTIVEA2
		global ACTIVEA3
		global ACTIVEA4
		global ACTIVEA5
		global ACTIVEA6
		global ACTIVEA7
		global ACTIVECATEGORYID

		ACTIVECATEGORYID = categoryid
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))
		rs = db.query('SELECT category as category,a1 as a1, a2 as a2, a3 as a3, a4 as a4, a5 as a5, a6 as a6, a7 as a7 FROM categories WHERE id = "%s";'%categoryid)
		for r in rs:

			ACTIVECATEGORY = r.category
			ACTIVEA1 = r.a1
			ACTIVEA2 = r.a2
			ACTIVEA3 = r.a3
			ACTIVEA4 = r.a4
			ACTIVEA5 = r.a5
			ACTIVEA6 = r.a6
			ACTIVEA7 = r.a7

		uzbl_cmd("js document.getElementById('scores_table').innerHTML='<tr><td id=s_cat style=font-size:250%%>%s</td></tr>'"%(web.websafe(ACTIVECATEGORY)))

		raise web.seeother('/manage')
		

#
# Audience
#

# uri: /playgame
# load thegame page
class playgame:
	def GET(self):
		return open("%s/%s"%(STATIC,'thegame.html'),"rb").read()

# uri: /attract
# load a page with a spining logo and playing the theme music
class attract:
	def GET(self):
		return open("%s/%s"%(STATIC,'attract.html'),"rb").read()

# uri: /silent
# load a simple page with nothing but the logo
class silent:
	def GET(self):
		return open("%s/%s"%(STATIC,'silent.html'),"rb").read()

# uri: /crash
# load a crash image
class crash:
	def GET(self):
		name = randomList(os.listdir(CRASHES))
		directory = "crashes"
		print "name: %s"%name[0]
		web.header("Cache-Control", "no-cache, max-age=0, no-store")
		render = web.template.render(STATIC)
		return render.crash(directory,name[0],3)

# uri: /bumper
# load a crash image
class bumper:
	def GET(self):
		name = randomList(os.listdir(BUMPERS))
		directory = "bumpers"

		print "name: %s"%name[0]
		web.header("Cache-Control", "no-cache, max-age=0, no-store")
		render = web.template.render(STATIC)
		return render.bumper(directory,name[0],3)
		

# uri: /commercial
#
# select a random commercial from the database,
# determine it's length
# play the commercial
# set the meta refresh to reload this page after the duration of the commercial has passed in seconds.
# if STOPCOMMERCIAL = True, then load the /silent page instead
class commercial:
	def GET(self):

		# since this is loaded each time
		# we can check to see if we need to stop using the flag
		# this will cause it to gracefully return to the silent banner page
		global STOPCOMMERCIALS
		if STOPCOMMERCIALS == True:
			STOPCOMMERCIALS = False
			raise web.seeother("/silent")

		# create the database and add the videos in VIDEOS directory
		if not os.path.isfile("%s/%s"%(BASE,"commercials.sqlite")):
			db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"commercials.sqlite"))
			db.query('create table commercials(filename char(200), seen char(1));')
			for name in os.listdir(VIDEOS):
				if name.split(".")[-1] == 'mp4':
					db.insert('commercials',filename = name, seen = 'N')
			db.close()

		# open the database
		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"commercials.sqlite"))
		
		#use the STATIC directory for rendering pages
		render = web.template.render(STATIC)

		r = db.query('SELECT filename as fn FROM commercials WHERE seen = "N" ORDER BY RANDOM() LIMIT 1;')

		try:
			# have all videos been seen?
			filename  = r[0].fn
		except IndexError:
			db.query('UPDATE commercials set seen = "N"')
			r = db.query('SELECT filename as fn FROM commercials WHERE seen = "N" ORDER BY RANDOM() LIMIT 1;')
			filename  = r[0].fn
			
		db.query('UPDATE commercials set seen = "Y" where filename = "%s"'%filename)
		duration = subprocess.Popen(['/usr/bin/mediainfo','--Output=Video;%Duration%',"%s/%s"%(VIDEOS,filename)], stdout=subprocess.PIPE).communicate()[0]
		duration = math.ceil(float(duration.rstrip())/1000)

		print("filename = |%s| Duration = |%s|"%(filename,duration))

		# this uses the "commercial.html" template with two parameters
		return render.commercial(filename,"%s"%str(int(duration)))

# uri: /show_scores
# 
# show the scores screen. sort by score.
# since there is technically no limit to the number of teams on
# the list, the sort will only show the top 15ish teams or so
class show_scores:
	def GET(self):
		# create the database
		if not os.path.isfile("%s/%s"%(BASE,"teamscores.sqlite")):
			return "There is no TEAM-SCORE DATABASE\n"

		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"teamscores.sqlite"))
		rs = db.query('select name as name,score as score from teamscores order by score DESC')

		l = []
		for r in rs:
			l.append(r)
		
		web.header("Cache-Control", "no-cache, max-age=0, no-store")
		render = web.template.render(STATIC)
		return render.show_scores(l,len(l))

# uri: /show_categories
#
# select 6 categories from the database. Give priority to categories that have
# a teamid equal to the ID associated with the active team
#
class show_categories:
	def GET(self):
		global CAT_HINTS
		# create the database
		if not os.path.isfile("%s/%s"%(BASE,"categories.sqlite")):
			return "There is no CATEGORIES DATABASE\n"

		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))

		# any affinity related categories?
		rs = db.query('select id as id, category as category, hint as hint, ord as ord from categories where teamid = "%s" and used = "N" order by ord limit 6'%(ACTIVETEAMID))

		cats = []

		for r in rs:
			cats.append(r)

		if len(cats) < 6 :
			rs = db.query('select id as id, category as category, hint as hint, ord as ord from categories where teamid = 0 and used = "N" order by ord limit %s'%(6-len(cats)))
			for r in rs:
				cats.append(r)
			
		randcats = randomList(cats)

		# for chosen categories, change ord to next highest number
		# get max ord number
		m = db.query('select max(ord) as o from categories')

		maxord = m[0].o

		print "Max ord is %s"%maxord
		
		c = 1
		for r in randcats:
			db.query('UPDATE categories set ord = %s where id = %s'%(maxord + c, r.id))
			c = c + 1

		CAT_HINTS = randcats
		print "Setting Hints: %s"%json.dumps(CAT_HINTS)

		render = web.template.render(STATIC)
		return render.show_categories(ACTIVETEAM, ACTIVESCORE,randcats,0)

#
# this is the big playgame loop and supporting functions you are looking for
# it will run as a separate thread. The funtions are used as an external timer.
# 
# Based the timer on this:
#
# http://pydev.blogspot.ca/2013/01/interrupting-python-thread-with-signals.html
#

class SigFinish(Exception):
	pass

def throw_signal_function(frame,event,arg):
	raise SigFinish()

def do_nothing_trace_function(frame,event,arg):
	# Note: each function called will actually call this function
	# so, take care, your program will run slower because of that.
	return None

def interrupt_thread(thread):
	for thread_id, frame in sys._current_frames().items():
		if thread_id == thread.ident:  # Note: Python 2.6 onwards
			set_trace_for_frame_and_parents(frame, throw_signal_function)

def set_trace_for_frame_and_parents(frame, trace_func):
	# Note: this only really works if there's a tracing function set in this
	# thread (i.e.: sys.settrace or threading.settrace must have set the
	# function before)
	while frame:
		if frame.f_trace is None:
			frame.f_trace = trace_func
		frame = frame.f_back
	del frame



class playthegame(threading.Thread):
	def __init__(self):
		super(playthegame, self).__init__()
		self.buzz = BUZZ
		self.score = 0
		self.db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"teamscores.sqlite"))

	def incrementscore(self,team_id):
		self.db.query("update teamscores set score = score + 1 where id = %s;"%team_id)


	def judging(self):
		print("Judging Routine")
		self.buzz.setlights(7)
		judges = [0,0,0]
		buttonresults = {'red':0,'blue':0,'orange':0}

		#read the controllers, and count the results
		while judges[0] == 0 or judges[1] == 0 or judges[2] == 0:
			r = self.buzz.readcontroller(timeout=50)
			if r != None:
				buttons = self.buzz.getbuttons()
				#for judge in range(len(buttons)):
				for judge in range(len(judges)):
					if buttons[judge]['red'] and judges[judge]==0:
						print("Judge %d, Button: Accept"%(int(judge)+1))
						judges[judge] = 1
						self.buzz.setlight(judge)
						buttonresults['red'] += 1
					if buttons[judge]['blue'] and judges[judge]==0:
						print("Judge %d, Button: Pass"%(int(judge)+1))
						judges[judge] = 2
						self.buzz.setlight(judge)
						buttonresults['blue'] += 1
					if buttons[judge]['orange'] and judges[judge]==0:
						print("Judge %d, Button: Deny"%(int(judge)+1))
						judges[judge] = 3
						self.buzz.setlight(judge)
						buttonresults['orange'] += 1
		print("Judges: %s"%json.dumps(judges))
						

		if buttonresults['red'] >= 2:
			print("Judges Accept")
			self.buzz.setlights(0)
			self.buzz.readcontroller(timeout=50)
			return("Accept")

		elif buttonresults['blue'] >= 2:
			print("Judges Passed")
			self.buzz.setlights(0)
			self.buzz.readcontroller(timeout=50)
			return("Pass")
	
		elif buttonresults['orange'] >= 2:
			print("Judges Rejected")
			self.buzz.setlights(0)
			self.buzz.readcontroller(timeout=50)
			return("Reject")

		elif buttonresults['red'] == 1 and buttonresults['blue'] == 1 and buttonresults['orange'] == 1:
			print("Judges Split")
			self.buzz.setlights(0)
			self.buzz.readcontroller(timeout=50)
			return("Split")
		

	def run(self):
		#load page
		answers_list = ['a1','a2','a3','a4','a5','a6','a7']

		#preload audio
		pygame.mixer.init()
		a_accept = pygame.mixer.Sound("%s/%s"%(ASSETS,"ding.ogg"))
		a_pass = pygame.mixer.Sound("%s/%s"%(ASSETS,"click.ogg"))
		a_reject = pygame.mixer.Sound("%s/%s"%(ASSETS,"cuckoo.wav"))
		a_split = pygame.mixer.Sound("%s/%s"%(ASSETS,"sad.ogg"))
		a_done = pygame.mixer.Sound("%s/%s"%(ASSETS,"buzzer.ogg"))

		db = web.database(dbn='sqlite',db="%s/%s"%(BASE,"categories.sqlite"))
		db.query('update categories set used = "Y" where id = %s'%ACTIVECATEGORYID)
		uzbl_cmd("set uri = http://localhost:8080/playgame")
		time.sleep(.1)
		uzbl_cmd("js document.getElementById('teamname').innerHTML='%s'"%web.websafe(ACTIVETEAM))
		time.sleep(.1)
		### because of the way that the background timer works, it seem prudent to keep this as tight as possible
		# start page counter
		uzbl_cmd('js window.checktimer();')
		sys.settrace(do_nothing_trace_function)

		# gotta catch the internal timer exceptions
		try:
			while len(answers_list)>0:
				answer = answers_list.pop()
				if answer == "a1":
					print("Showing a1")
					#set answer
					uzbl_cmd("js document.getElementById('maintext').innerHTML='%s'"%web.websafe(ACTIVEA1))

					# read the controllers
					decision = self.judging()
					# determine judge responses
					if decision == "Accept":
						# adust score
						self.incrementscore(ACTIVETEAMID)
						# play sound
						a_accept.play()
					elif decision == "Pass":
						answers_list.append('a1')
						# play sound
						a_pass.play()
					elif decision == "Reject":
						# play sound
						a_reject.play()
					elif decision == "Split":
						# play sound
						a_split.play()
					time.sleep(.1)

				elif( answer == "a2"):
					print("Showing a2")
					# set answer
					uzbl_cmd("js document.getElementById('maintext').innerHTML='%s'"%web.websafe(ACTIVEA2))
					# read the controllers
					decision = self.judging()
					# determine judge responses
					if decision == "Accept":
						# adust score
						self.incrementscore(ACTIVETEAMID)
						# play sound
						a_accept.play()
					elif decision == "Pass":
						answers_list.append('a1')
						# play sound
						a_pass.play()
					elif decision == "Reject":
						# play sound
						a_reject.play()
					elif decision == "Split":
						# play sound
						a_split.play()
					time.sleep(.1)

				elif( answer == "a3"):
					print("Showing a3")
					# set answer
					uzbl_cmd("js document.getElementById('maintext').innerHTML='%s'"%web.websafe(ACTIVEA3))
					# read the controllers
					decision = self.judging()
					# determine judge responses
					if decision == "Accept":
						# adust score
						self.incrementscore(ACTIVETEAMID)
						# play sound
						a_accept.play()
					elif decision == "Pass":
						answers_list.append('a1')
						# play sound
						a_pass.play()
					elif decision == "Reject":
						# play sound
						a_reject.play()
					elif decision == "Split":
						# play sound
						a_split.play()
					time.sleep(.1)
				elif( answer == "a4"):
					print("Showing a4")
					# set answer
					uzbl_cmd("js document.getElementById('maintext').innerHTML='%s'"%web.websafe(ACTIVEA4))
					# read the controllers
					decision = self.judging()
					# determine judge responses
					if decision == "Accept":
						# adust score
						self.incrementscore(ACTIVETEAMID)
						# play sound
						a_accept.play()
					elif decision == "Pass":
						answers_list.append('a1')
						# play sound
						a_pass.play()
					elif decision == "Reject":
						# play sound
						a_reject.play()
					elif decision == "Split":
						# play sound
						a_split.play()
					time.sleep(.1)
				elif( answer == "a5"):
					print("Showing a5")
					# set answer
					uzbl_cmd("js document.getElementById('maintext').innerHTML='%s'"%web.websafe(ACTIVEA5))
					# read the controllers
					decision = self.judging()
					# determine judge responses
					if decision == "Accept":
						# adust score
						self.incrementscore(ACTIVETEAMID)
						# play sound
						a_accept.play()
					elif decision == "Pass":
						answers_list.append('a1')
						# play sound
						a_pass.play()
					elif decision == "Reject":
						# play sound
						a_reject.play()
					elif decision == "Split":
						# play sound
						a_split.play()
					time.sleep(.1)
				elif( answer == "a6"):
					print("Showing a6")
					# set answer
					uzbl_cmd("js document.getElementById('maintext').innerHTML='%s'"%web.websafe(ACTIVEA6))
					# read the controllers
					decision = self.judging()
					# determine judge responses
					if decision == "Accept":
						# adust score
						self.incrementscore(ACTIVETEAMID)
						# play sound
						a_accept.play()
					elif decision == "Pass":
						answers_list.append('a1')
						# play sound
						a_pass.play()
					elif decision == "Reject":
						# play sound
						a_reject.play()
					elif decision == "Split":
						# play sound
						a_split.play()
					time.sleep(.1)
				elif( answer == "a7"):
					print("Showing a7")
					# set answer
					uzbl_cmd("js document.getElementById('maintext').innerHTML='%s'"%web.websafe(ACTIVEA7))
					# read the controllers
					decision = self.judging()
					# determine judge responses
					if decision == "Accept":
						# adust score
						self.incrementscore(ACTIVETEAMID)
						# play sound
						a_accept.play()
					elif decision == "Pass":
						answers_list.append('a1')
						# play sound
						a_pass.play()
					elif decision == "Reject":
						# play sound
						a_reject.play()
					elif decision == "Split":
						# play sound
						a_split.play()
					time.sleep(.1)

		except SigFinish:
			print("Finishing on Interrupt Signal")
			#uzbl_cmd("js window.done.play();")
			a_done.play()
			time.sleep(1)
			self.buzz.setlights(0)
			self.stop()

		print("finishing with out interrupt")
		time.sleep(.5)
		self.buzz.setlights(0)
		self.stop()

	def stop(self):
		try:
			#UpdateScore
			if self.score == 7:
				uzbl_cmd("js document.getElementById('maintext').innerHTML='FULL RUN!'")
				uzbl_cmd("js document.getElementById('maintext').style.color='green'")
				time.sleep(3)
				uzbl_cmd("set uri = http://localhost:8080/show_scores")
			else:
				uzbl_cmd("set uri = http://localhost:8080/show_scores")
				time.sleep(1)
				print("Exiting playthegame thread")
		except SigFinish:
			a_done.play()
			#uzbl_cmd("js window.done.play();")
			uzbl_cmd("set uri = http://localhost:8080/show_scores")
			time.sleep(1)
			print("Exiting playthegame thread")
	


		

#
# assets
#

# uri: /videos/(.*)
# this will get (.*) as "name" try and determin the filetype by extention, set the mimetypem and feed back
# the contents of the file to the browser
class videos:
	def GET(self,name):
		ext = name.split(".")[-1]

		ctype = {
			"mp4":"video/mp4"
			}

		if name in os.listdir(VIDEOS):
			web.header("Content-Type", ctype[ext])
			return open("%s/%s"%(VIDEOS,name),"rb").read()

# uri: /assets/(.*)
# this will get (.*) as "name" try and determin the filetype by extention, set the mimetypem and feed back
# the contents of the file to the browser
class assets:
	def GET(self,name):
		ext = name.split(".")[-1]

		ctype = {
			"png":"images/png",
			"jpg":"images/jpeg",
			"gif":"images/gif",
			"mp3":"audio/mpeg",
			"wav":"audio/wav",
			"ico":"images/ico"
			}

		if name in os.listdir(ASSETS):
			web.header("Content-Type", ctype[ext])
			return open("%s/%s"%(ASSETS,name),"rb").read()

# uri: /crashes/(.*)
class crashes:
	def GET(self,name):
		ext = name.split(".")[-1]

		ctype = {
			"png":"images/png",
			"jpg":"images/jpeg",
			"gif":"images/gif",
			"mp3":"audio/mpeg",
			"wav":"audio/wav",
			"ico":"images/ico"
			}

		if name in os.listdir(CRASHES):
			web.header("Content-Type", ctype[ext])
			return open("%s/%s"%(CRASHES,name),"rb").read()

# uri: /bumpers/(.*)
class bumpers:
	def GET(self,name):
		ext = name.split(".")[-1]

		ctype = {
			"png":"images/png",
			"jpg":"images/jpeg",
			"gif":"images/gif",
			"mp3":"audio/mpeg",
			"wav":"audio/wav",
			"ico":"images/ico"
			}

		if name in os.listdir(BUMPERS):
			web.header("Content-Type", ctype[ext])
			return open("%s/%s"%(BUMPERS,name),"rb").read()

#
# utilities
#

def randomList(a):
	b = []
	for i in range(len(a)):
		element = random.choice(a)
		a.remove(element)
		b.append(element)
	return b

# this is the primary communication channel for talking to uzbl
# it is globally available
def uzbl_cmd(commands):
	global sockpath
	sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	sock.connect(sockpath)
#	for command in commands:
	print("Sending = |%s|"%commands)
	sock.send('%s' %commands)
	sock.close()


#
# main
#

if __name__ == '__main__':

	# this is the base directory, it is primarily used to locate the binary, and hp.conf for uzbl
	# it will also be the location of the sqlite3 databases
	BASE = '/home/als/hackerpyramid/NewHackerPyramid/'
	# assets contains pictures, music and sounds
	ASSETS = '%s/assets/'%BASE
	# static is the templates directory
	STATIC = '%s/static/'%BASE
	# crashes contains the images of crashes
	CRASHES = '%s/crashes/'%BASE
	# bumpers contains the images before commercials
	BUMPERS = '%s/bumpers/'%BASE
	# videos is where the commercials are
	VIDEOS = '/home/als/Videos/retro/'

	try:
		BUZZ = buzz.buzz()
	except Exception, e:
		print e
		

	STOPCOMMERCIALS = False
	ACTIVETEAM = ""
	ACTIVETEAMID = ""
	ACTIVESCORE = ""
	ACTIVECATEGORY = ""
	ACTIVEA1 = ""
	ACTIVEA2 = ""
	ACTIVEA3 = ""
	ACTIVEA4 = ""
	ACTIVEA5 = ""
	ACTIVEA6 = ""
	ACTIVEA7 = ""
	ACTIVECATEGORYID = ""
	CAT_HINTS = ""

	p = subprocess.Popen(['/usr/bin/uzbl-core','--geometry','1920x1080','-c','%s/hp.conf'%BASE],cwd="/",stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	sockpath = "/tmp/uzbl_socket_%s"%p.pid

	print("socket at |%s|"%sockpath)

	urls = (
		'/assets/(.*)','assets',
		'/videos/(.*)','videos',
		'/crashes/(.*)','crashes',
		'/bumpers/(.*)','bumpers',
		'/crash','crash',
		'/bumper','bumper',
		'/manage','management',
		'/editor','editor',
		'/commercial','commercial',
		'/intro', 'intro',
		'/attract', 'attract',
		'/silent', 'silent',
		'/playgame', 'playgame',
		'/load_playgame','load_playgame',
		'/load_showcategories','load_showcategories',
		'/load_commercials','load_commercials',
		'/load_crash','load_crash',
		'/stop_commercials','stop_commercials',
		'/reset_commercials','reset_commercials',
		'/reset_categories','reset_categories',
		'/load_silent','load_silent',
		'/load_scores','load_scores',
		'/load_attract','load_attract',
		'/set_team/(.*)','set_team',
		'/inc_score/(.*)','inc_score',
		'/dec_score/(.*)','dec_score',
		'/set_used/(.*)','set_used',
		'/set_unused/(.*)','set_unused',
		'/set_category/(.*)','set_category',
		'/show_categories','show_categories',
		'/show_scores','show_scores',
		'/team_add','team_add',
		'/team_edit/(.*)','team_edit',
		'/team_delete/(.*)','team_delete',
		'/category_add','category_add',
		'/category_delete/(.*)','category_delete',
		'/category_edit/(.*)','category_edit',
		'/affinity_inc/(.*)','affinity_inc',
		'/affinity_dec/(.*)','affinity_dec',
		'/hints','hints'
	)


	app = web.application(urls, globals())
	try:
		app.run()
		#uzbl_cmd('set uri = http://localhost:8080/attract')
	except KeyboardInterrupt:
		uzbl_cmd('exit',sockpath)
		
	

# Notes for things not to forget

# echo 'js document.getElementById("score").innerHTML="35"' | socat - /tmp/uzbl_socket_5730
# echo 'js window.pass.play();' | socat - /tmp/uzbl_socket_5730

# start at 25% padding, and drop by 25% for every line. A line is 28 characters max at 200% font size
# echo 'js document.getElementById("maintext").innerHTML="123456789 123456789 123456789 123456789 123456789 123456789";document.getElementById("maintext").style.padding="15% 0";'

# pygame.mixer.init()
# pygame.mixer.music.load("file.mp3")
# pygame.mixer.music.play()
# pygame.mixer.Sound("file.mp3").play()

