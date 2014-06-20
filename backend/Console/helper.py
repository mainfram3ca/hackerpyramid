import curses, time

states = ["Showing Penny", "Showing Video", "Showing Catagories", "Round Running"]
messages = []

def fill(window, ch):
    y, x = window.getmaxyx()
    s = ch * (x - 1)
    for line in range(y):
        window.addstr(line, 0, s)


def SetState(State, topscr):
    # curses.cbreak() # Don't wait for enter
    fill(topscr, " ")
    txtstate = "State: %s" % states[State]
    topscr.addstr(0, 0, txtstate)
    topscr.addstr(0, 30 , "|")
    topscr.refresh()

def SetTime(Timer, timescr):
    # curses.cbreak() # Don't wait for enter
    fill(timescr, " ")
    txtstate = "Time: %s" % Timer
    timescr.addstr(0, 0, txtstate)
#    timescr.addstr(0, 30 , "|")
    timescr.refresh()

def SetLog(Message, logscr):
    messages.append(Message)
    num=0
    logscr.erase()
    for message in messages[-9:]:
	logscr.addstr(num,0,message)
	num += 1
    logscr.refresh()

def DefineColours():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

def ShowContestants(window):
    contscr = curses.newwin(15,45,10,10)
    contscr.bkgd(' ', curses.color_pair(1))
    contscr.border()
    contscr.addstr(0,14, "Select Contestant")
    contscr.refresh()
    time.sleep(1)
    del contscr
    window.touchwin()
    window.refresh()

def ShowCatagories(window):
    contscr = curses.newwin(15,45,10,10)
    contscr.bkgd(' ', curses.color_pair(1))
    contscr.border()
    contscr.addstr(0,15, "Select Catagory")
    contscr.addstr(12,2, "(Q)uit without Selecting")
    contscr.addstr(13,2, "Select:")
    contscr.refresh()
    while 1:
	c = contscr.getch()
	if c == ord('q'):
	    break
    del contscr
    window.touchwin()
    window.refresh()
