#!/usr/bin/python

# USB handler 
# Handles keyboard? commands from judges/contestant buttons.

# Judges (Need 2 out of 3 to trigger)
# CORRECT: 1 2 3
# FAIL: A B C

# Contestant
# PASS: P

import MySQLdb

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="john", # your username
                      passwd="megajonhy", # your password
                      db="jonhydb") # name of the data base

cur = db.cursor() 
cur.execute("SELECT * FROM YOUR_TABLE_NAME")

