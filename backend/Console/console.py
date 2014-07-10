#!/usr/bin/env python
# The main program
# This handles the text console for the administrator, as well as handles the Buzz! controllers

import curses, traceback, time, database, json, websocket
import database, buzz
from helper import *
from catagories import catagories

Debug = True
roundlength = 30
state = 0
team = False

db = database.pyrDB()
buzz = buzz.buzz()
cataclass = catagories(db)

# The Main two functions -- addtional functions for other screens are elsewhere
# Function - Off Round
def OffRound(window):
    global state, messages, db, team
    # curses.cbreak() # Don't wait for enter
    SetTime(0)
    stdscr.addstr(3,0, "1 - Show Penny")
    stdscr.addstr(4,0, "2 - Select Contestants")
    stdscr.addstr(5,0, "3 - Show Catagories")
    stdscr.addstr(7,0, "4 - Start/Stop Videos")
    stdscr.addstr(8,0, "5 - Start/Stop Theme")
    stdscr.addstr(9,0, "6 - Start/Stop Timer")
    stdscr.addstr(11,0, "R - Run Round")
    stdscr.addstr(12,0, "Q - Quit")
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
	SetLog("Showing Contestants")
	laststate = state
	state = 4
	SetState(state)
	team = SelectTeams(window)
	if team != False:
	    SetCataTeam(cataclass.GetCatagory(), team)
	    SetLog("Selected Team: %s" % team['Name'])
	    if Debug: SetLog(" - %s" % dict(zip(team.keys(), team)), True)
	else:
	    SetCataTeam(cataclass.GetCatagory(), False)
	    SetLog("Team Not Selected")
	state = laststate
	SetState(state, False)
    elif c == ord('3'):
	if (team == False):
	    ShowError("Select a team first")
	else:
	    SetLog("Showing Catagories")
	    state = 2
	    SetState(state)
	    catagory = SelectCatagories(db, team['id'])
	    if catagory != False:
		SetCataTeam(cataclass.GetCatagory(), team)
		SetLog("Selected Catagory: %s" % catagory['Title'])
		if Debug: SetLog( " - %s" % dict(zip(catagory.keys(), catagory)), True)
	    else:
		SetCataTeam(cataclass.GetCatagory(), False)
		SetLog("Catagory Not Selected")
	    state = 0
	    SetState(state)
    elif c == ord('4'):
	if GetState() == 1:
	    state = 5
	    SetState(state, False)
	else:
	    SetLog("Showing Video")
	    playVideo()
	    state = 1
	    SetState(state)
    elif c == ord('5'):
	playFX("theme", True)
    elif c == ord('6'):
	StartRunTime()
    return 1

# Function - Run Round
def RunRound():
    global state
    if cataclass.GetCatagory() == None or team == False:
	SetLog("ERROR: Catagory or Team is not set!")
	return False
    # TODO: We're running a round, Need to mark the catagory used
    # Read the controllers to clear them.
    buzz.readcontroller(timeout=50)
    buttonresults = [0,0,0]
    judges = [0,0,0,0]
    reset = 0
    # Set the lights on the controllers to on
    buzz.setlights(15)
    state = 3
    SetState(state)
    # Get the current time, and find out how much time has past.
    start = time.time()
    timer = round (roundlength + start - time.time(), 2)
    SetAnswer()
    while timer > 0:
	# Read the controllers
	r = buzz.readcontroller(timeout=50)
	if r != None:
	    # At least one button was pressed - find out what
	    buttons = buzz.getbuttons()
	    for judge in range(len(buttons)):
		# If the judge hasn't responded yet, set their response
		if judges[judge] == 0 and not reset:
		    if buttons[judge]['red']:
			SetLog("Judge: %d, Button: Accept" % (int(judge) + 1))
			judges[judge] = 1
			buzz.setlight(judge)
			buttonresults[0] += 1
		    if buttons[judge]['blue']:
			SetLog("Judge: %d, Button: Pass" % (int(judge) + 1))
			judges[judge] = 2
			buzz.setlight(judge)
			buttonresults[1] += 1
		    if buttons[judge]['orange']:
			SetLog("Judge: %d, Button: Deny" % (int(judge) + 1))
			judges[judge] = 3
			buzz.setlight(judge)
			buttonresults[2] += 1
	    # If 2/3 judges agree, accept it
	    if not reset:
		if buttonresults[0] >= 2:
		    playFX("ding")
		    db.IncrementScore(team['id'])
		    cataclass.Judged(1)
		    buzz.setlights(0)
		    reset = time.time()
		    SetLog("Judges Accept!")
		    result = SetAnswer()
		    if result == None:
			break
		elif buttonresults[1] >= 2:
		    cataclass.Judged(2)
		    buzz.setlights(0)
		    reset = time.time()
		    SetLog("Judges Passed!")
		    result = SetAnswer()
		    if result == None:
			break
		elif buttonresults[2] >= 2:
		    playFX("wrong")
		    cataclass.Judged(3)
		    buzz.setlights(0)
		    reset = time.time()
		    SetLog("Judges Denied!")
		    result = SetAnswer()
		    if result == None:
			break
		elif buttonresults[0] == 1 and buttonresults[1] == 1 and buttonresults[2] == 1:
		# If we have 3 different selects, reset the judges
		    buttonresults = [0,0,0]
		    judges = [0,0,0,0]
		    reset = 0
		    for x in range(4):
			buzz.setlights(15)
			time.sleep(.05)
			buzz.setlights(0)
			time.sleep(.05)
		    buzz.setlights(15)
		    SetLog("Split Judges!")
	if (reset and time.time() - reset > .5):
	    # Check RESET state (timestamp) for .5 seconds then reset the judges
	    # Read the controllers to clear them.
	    buzz.readcontroller(timeout=50)
	    buttonresults = [0,0,0]
	    judges = [0,0,0,0]
	    results = 0
	    reset = 0
	    buzz.setlights(15)
	SetTime("%.3f" % timer)
	timer = round (roundlength + start - time.time(), 2)
    playFX("buzzer")
    state = 0
    cataclass.Clear()
    SetCataTeam(cataclass.GetCatagory(), team)
    SetState(state)
    # TODO: Send end of round stats
    buzz.setlights(0)

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

      for x in range(16):
        buzz.setlights(x)
        time.sleep(.1)
      buzz.setlights(0)

      # Make the websocket available to the helper modules
      setws(ws, db, buzz, cataclass)

      DefineColours()
      y, x = stdscr.getmaxyx()
      topscr=stdscr.subwin(1,x-45,0,0)
      runtimescr=stdscr.subwin(1,30,0,x-45)
      timescr=stdscr.subwin(1,15,0,x-15)
      infoscr=stdscr.subwin(1,x,1,0)
      logscr=stdscr.subwin(11,x,y-11,0)
      teamsscr=stdscr.subwin(15,45,4,x-50)

      topscr.bkgd(' ', curses.color_pair(1))
      runtimescr.bkgd(' ', curses.color_pair(2))
      timescr.bkgd(' ', curses.color_pair(1))
      infoscr.bkgd(' ', curses.color_pair(1))
      logscr.bkgd(' ', curses.color_pair(1))
      teamsscr.bkgd(' ', curses.color_pair(1))

      logscr.border()
      teamsscr.border()

      setscreens (stdscr, topscr, timescr,logscr,infoscr, teamsscr, runtimescr)

      SetCataTeam(None, False)
      # Turn off echoing of keys, and enter cbreak mode,
      # where no buffering is performed on keyboard input
      curses.noecho()
      curses.cbreak()

      # Start the Timing thread
      RunTimer()
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
