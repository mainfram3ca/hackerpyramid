import curses

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
