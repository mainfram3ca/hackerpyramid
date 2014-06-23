#!/usr/bin/env python
# The main program
# This handles the text console for the administrator, as well as handles the Buzz! controllers

import curses, traceback, time, database, websocket, json
from helper import *

state = 0
db = database.pyrDB()
catagory = False
team = False
Debug = True

# The Main two functions -- addtional functions for other screens are elsewhere
# Function - Off Round
def OffRound(window):
    global state, messages, db, catagory, team
    # curses.cbreak() # Don't wait for enter
    UpdateTeams(window, db)
    SetTime(0)
    stdscr.addstr(3,0, "Q - Quit")
    stdscr.addstr(4,0, "1 - Show Penny")
    stdscr.addstr(5,0, "2 - Show Video")
    stdscr.addstr(6,0, "3 - Show Catagories")
    stdscr.addstr(7,0, "4 - Select Contestants")
    stdscr.addstr(8,0, "5 - Start/Stop Theme")
    stdscr.addstr(9,0, "R - Run Round")
    c = stdscr.getch()
    if c == ord ('r'):
	SetLog("Running Round")
	RunRound()
    elif c == ord('q'):
	return 0
    elif c == ord('1'):
	SetLog("Showing Penny")
	state = 0
	SetState(state)
    elif c == ord('2'):
	SetLog("Showing Video")
	playVideo()
	state = 1
	SetState(state)
    elif c == ord('3'):
	SetLog("Showing Catagories")
	state = 2
	SetState(state)
	catagory = SelectCatagories(window, db)
	if catagory != False:
	    SetCataTeam(catagory, team)
	    SetLog("Selected Catagory: %s" % catagory['Title'])
	    if Debug: print " -", catagory
	else:
	    SetCataTeam(False, team)
	    SetLog("Catagory Not Selected")
	state = 0
	SetState(state)
    elif c == ord('4'):
	SetLog("Showing Contestants")
	laststate = state
	state = 4
	SetState(state)
	team = SelectTeams(window, db)
	if team != False:
	    SetCataTeam(catagory, team)
	    SetLog("Selected Team: %s" % team['Name'])
	    if Debug: print " -", team
	else:
	    SetCataTeam(catagory, False, statescr)
	    SetLog("Team Not Selected")
	state = laststate
	SetState(state, False)
    elif c == ord('5'):
	playFX("theme", True)
    return 1

# Function - Run Round
def RunRound():
    global state
    if catagory == False or team == False:
	SetLog("ERROR: Catagory or Team is not set!")
	return False
    state = 3
    SetState(state)
    # Get the current time, and find out how much time has past... for now, we sleep :)
    start = time.time()
    timer = 1
    while timer > 0:
	SetTime("%.3f" % timer)
	timer = round (10 + start - time.time(), 2)
    playFX("buzzer")
    state = 0

def main(window): 
    Running = 1 
    while Running:
	Running = OffRound(window)


if __name__=='__main__':
  print "Running..."
  try:
      # Initialize curses
      stdscr=curses.initscr()
      ws = websocket.EchoClient('ws://localhost:9000/ws')
      ws.daemon = False
      ws.connect()

      # Make the websocket available to the helper modules
      setws(ws)

      DefineColours()
      y, x = stdscr.getmaxyx()
      topscr=stdscr.subwin(1,x-15,0,0)
      timescr=stdscr.subwin(1,15,0,x-15)
      infoscr=stdscr.subwin(1,x,1,0)
      logscr=stdscr.subwin(10,x,y-10,0)
      topscr.bkgd(' ', curses.color_pair(1))
      timescr.bkgd(' ', curses.color_pair(1))
      infoscr.bkgd(' ', curses.color_pair(1))

      setscreens (topscr, timescr,logscr,infoscr)

      SetCataTeam(catagory, team)
      # Turn off echoing of keys, and enter cbreak mode,
      # where no buffering is performed on keyboard input
      curses.noecho()
      curses.cbreak()

      # In keypad mode, escape sequences for special keys
      # (like the cursor keys) will be interpreted and
      # a special value like curses.KEY_LEFT will be returned
      # stdscr.keypad(1)
      main(stdscr)                    # Enter the main loop
      # Set everything back to normal
      ws.close(reason=json.dumps(["Gone"]))
      stdscr.keypad(0)
      curses.echo()
      curses.nocbreak()
      curses.endwin()                 # Terminate curses
  except:
      # In event of error, restore terminal to sane state.
      ws.close()
      stdscr.keypad(0)
      curses.echo()
      curses.nocbreak()
      curses.endwin()
      traceback.print_exc()           # Print the exception
