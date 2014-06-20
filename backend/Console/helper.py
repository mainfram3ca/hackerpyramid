import curses, time, json

states = ["Showing Penny", "Showing Video", "Showing Catagories", "Round Running"]
messages = []

def setws(rws):
    global ws
    ws = rws

def fill(window, ch):
    y, x = window.getmaxyx()
    s = ch * (x - 1)
    for line in range(y):
        window.addstr(line, 0, s)

def SetState(State, topscr):
    # curses.cbreak() # Don't wait for enter
    ws.sendMessage(json.dumps(dict(state= State)))
    fill(topscr, " ")
    txtstate = "State: %s" % states[State]
    topscr.addstr(0, 0, txtstate)
#    topscr.addstr(0, 30 , "|")
    topscr.refresh()

def SetTime(Timer, timescr):
    # curses.cbreak() # Don't wait for enter
    fill(timescr, " ")
    txtstate = "Time: %s" % Timer
    timescr.addstr(0, 0, txtstate)
#    timescr.addstr(0, 30 , "|")
    timescr.refresh()

def SetCataTeam(catagory, team, statescr):
    y, x = statescr.getmaxyx()
    fill(statescr, " ")
    if catagory == False:
	catagory = ""
    else:
	catagory = catagory['Title']
    if team == False:
	team = ""
    else:
	team = team['Name']
    txtcata = "Catagory: %s" % catagory
    txtteam = "Team: %s" % team
    statescr.addstr(0,0, txtcata)
    statescr.addstr(0,x-60, txtteam)
    statescr.refresh()

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

def ShowCatagories(window, db):
    contscr = curses.newwin(15,45,10,10)
    contscr.bkgd(' ', curses.color_pair(1))
    contscr.border()
    catagories = db.GetCatagories()
    contscr.addstr(0,15, "Select Catagory")
    count = 0
    for row in catagories:
        contscr.addstr(3+count,2, "%d - %s " % (1+count, row["title"]))
	count += 1 
    contscr.addstr(12,2, "(Q)uit without Selecting")
    contscr.addstr(13,2, "Select:")
    contscr.refresh()
    while 1:
	c = contscr.getch()
	if c == ord('q'):
	    result = False
	    break
	try:
	    result = catagories[c-49]
	    break
	except IndexError:
	    pass

    del contscr
    window.touchwin()
    window.refresh()
    return result

def ShowTeams(window, db):
    contscr = curses.newwin(15,45,10,10)
    contscr.bkgd(' ', curses.color_pair(1))
    contscr.border()
    teams = db.GetTeams()
    contscr.addstr(0,15, "Select Team")
    count = 0
    for row in teams:
        contscr.addstr(3+count,2, "%d - %s " % (1+count, row["Name"]))
	count += 1 
    contscr.addstr(12,2, "(Q)uit without Selecting")
    contscr.addstr(13,2, "Select:")
    contscr.refresh()
    while 1:
	c = contscr.getch()
	if c == ord('q'):
	    result = False
	    break
	try:
	    result = teams[c-49]
	    break
	except IndexError:
	    pass

    del contscr
    window.touchwin()
    window.refresh()
    return result
