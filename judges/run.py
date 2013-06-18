#!/usr/bin/python

# USB handler 
# Handles keyboard? commands from judges buttons.

import MySQLdb

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="john", # your username
                      passwd="megajonhy", # your password
                      db="jonhydb") # name of the data base

cur = db.cursor() 
cur.execute("SELECT * FROM YOUR_TABLE_NAME")