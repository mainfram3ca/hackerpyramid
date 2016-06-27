# Database Handler

import sqlite3 as lite

class pyrDB:

	def __init__(self):
		# Load the Database
		self.database = lite.connect("database.sqlite")
		self.database.row_factory = lite.Row
		self.cur = self.database.cursor()

	def GetNextVideo(self):
		# get a random video
		self.cur.execute("SELECT filename FROM videos WHERE used != 1 ORDER BY RANDOM() LIMIT 1")
		v = self.cur.fetchone()

		# if there are no videos to get, reset the used flag and try again
		# if after rest there is still None it will return None
		if (v == None):
			self.cur.execute("UPDATE videos SET used = 0")
			self.database.commit()
			self.cur.execute("SELECT filename FROM videos WHERE used != 1 ORDER BY RANDOM() LIMIT 1")
			v = self.cur.fetchone()
			if (v != None):
				self.cur.execute("UPDATE videos SET used = 1 WHERE filename = ?",(v,))
			if (v == None):
				return(v)
			else:
				return(v[0])
		else:
			return(v[0])

	def GetCatagories(self, team):
		# The number of catagories we need
		catareq = 5
		catagories = []
		# Check for Pre-selected catagories
		self.cur.execute("SELECT * FROM catagories WHERE used != 1 AND preselect == -1")
		for cata in self.cur.fetchall():
		    catagories.append(cata)
		catareq = catareq - len(catagories)

		# Check for Team Trap Catagories
		counter = 0
		self.cur.execute("SELECT * FROM catagories WHERE used != 1 AND preselect == %d" % team)
		for cata in self.cur.fetchall():
		    catagories.append(cata)
		    counter += 1
		catareq = catareq - counter

		# Select Random Catagories
		self.cur.execute("SELECT * FROM catagories WHERE used != 1 AND preselect == 0 ORDER BY RANDOM() LIMIT %d" % catareq)
		for cata in self.cur.fetchall():
		    catagories.append(cata)
		return catagories

	def GetTeams(self):
		# Select Teams
		self.cur.execute("SELECT * FROM teams WHERE active = 1")
		return self.cur.fetchall()

	def IncrementScore(self, team):
		self.cur.execute('''UPDATE teams SET score=score+1 WHERE id = ?''', (team,))
		self.database.commit()

	def UseCatagory(self, catagory):
		self.cur.execute('''UPDATE catagories SET used = 1 WHERE id = ?''', (catagory,))
		self.database.commit()

	def close(self):
		self.database.close()
