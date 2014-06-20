#!/usr/bin/env python
# The main program
# This handles the text console for the administrator, as well as handles the Buzz! controllers

import curses, traceback, time
from helper import *

state = 0

def fill(window, ch):
    y, x = window.getmaxyx()
    s = ch * (x - 1)
    for line in range(y):
        window.addstr(line, 0, s)

# The Main two functions -- addtional functions for other screens are elsewhere
# Function - Off Round
def OffRound():
    global state, messages
    # curses.cbreak() # Don't wait for enter
    SetState(state, topscr)
    SetTime(0, timescr)
    stdscr.addstr(2,0, "Q - Quit")
    stdscr.addstr(3,0, "1 - Show Penny")
    stdscr.addstr(4,0, "2 - Show Video")
    stdscr.addstr(5,0, "3 - Show Catagories")
    stdscr.addstr(6,0, "R - Run Round")
    c = stdscr.getch()
    if c == ord ('r'):
	SetLog("Running Round", logscr)
	RunRound()
    elif c == ord('q'):
	return 0
    elif c == ord('1'):
	SetLog("Showing Penny", logscr)
	state = 0
    elif c == ord('2'):
	SetLog("Showing Video", logscr)
	state = 1
    elif c == ord('3'):
	SetLog("Showing Catagories", logscr)
	state = 2
    return 1

# Function - Run Round
def RunRound():
    global state
    state = 3
    SetState(state, topscr)
    # Get the current time, and find out how much time has past... for now, we sleep :)
    start = time.time()
    timer = 1
    while timer > 0:
	SetTime("%s" % timer, timescr)
	# SetLog("Time: %s" % timer, logscr)
	# time.sleep(.250)
	timer = round (10 + start - time.time(), 2)
    state = 0

def main(window): 
    Running = 1 
    while Running:
	Running = OffRound()


if __name__=='__main__':
  print "Running..."
  try:
      # Initialize curses
      stdscr=curses.initscr()

      DefineColours()
      y, x = stdscr.getmaxyx()
      topscr=stdscr.subwin(1,x-15,0,0)
      timescr=stdscr.subwin(1,15,0,x-15)
      logscr=stdscr.subwin(10,x,y-10,0)
      topscr.bkgd(' ', curses.color_pair(1))
      timescr.bkgd(' ', curses.color_pair(1))

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
      stdscr.keypad(0)
      curses.echo()
      curses.nocbreak()
      curses.endwin()                 # Terminate curses
  except:
      # In event of error, restore terminal to sane state.
      stdscr.keypad(0)
      curses.echo()
      curses.nocbreak()
      curses.endwin()
      traceback.print_exc()           # Print the exception
