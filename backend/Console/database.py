# Database Handler

import sqlite3 as lite

class pyrDB:

    def __init__(self):
	# Load the Database
	self.database = lite.connect("database.sqlite")
	self.database.row_factory = lite.Row
	self.cur = self.database.cursor()

    def GetCatagories(self):
	# TODO: Should check for Celeb Trap Catagories First
	# Select Random Catagories
	catareq = 5
	self.cur.execute("SELECT * FROM catagories WHERE used != 1 ORDER BY RANDOM() LIMIT %d" % catareq)
	return self.cur.fetchall()
