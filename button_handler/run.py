#!/usr/bin/python

# USB handler 
# Handles keyboard? commands from judges/contestant buttons.

# Judges (Need 2 out of 3 to trigger)
# CORRECT: 1 2 3
# FAIL: A B C

# Contestant
# PASS: P

db="coolacid_10k";                                                                                              
dbuser="coolacid_10k";                                                                                          
dbpass="N;dXvCP6POy&";

import MySQLdb

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user=dbuser, # your username
                      passwd=dbpass, # your password
                      db=db) # name of the data base

cur = db.cursor() 
cur.execute("SELECT * FROM status")

for row in cur.fetchall() :
    print row

# Should check to see if there is time left before awarding points. (Race condition)