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

class _Getch:
    """
	Gets a single character from standard input.  Does not echo to the screen.

	FROM: http://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/

    """
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user=dbuser, # your username
                      passwd=dbpass, # your password
                      db=db) # name of the data base

cur = db.cursor() 
cur.execute("SELECT * FROM status")

for row in cur.fetchall() :
    print row

print getch()

# Should check to see if there is time left before awarding points. (Race condition)