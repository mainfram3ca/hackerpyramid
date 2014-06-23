import curses, time, json

states = ["Showing Penny", "Showing Video", "Showing Catagories", "Round Running", "Select Team"]
messages = []
screens = {}
lasttime = 0

def setws(rws):
    global ws
    ws = rws

def setscreens(top, time, log, info):
    screens['top'] = top
    screens['time'] = time
    screens['log'] = log
    screens['info'] = info

def DefineColours():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)

def fill(window, ch):
    y, x = window.getmaxyx()
    s = ch * (x - 1)
    for line in range(y):
        window.addstr(line, 0, s)

def SetState(State, broadcast=True):
    topscr = screens['top']
    if broadcast:
	ws.sendMessage(json.dumps(dict(state=State)))
    fill(topscr, " ")
    txtstate = "State: %s" % states[State]
    topscr.addstr(0, 0, txtstate)
    topscr.refresh()

def SetTime(Timer, broadcast=True):
    global lasttime
    timescr = screens['time']
    roundtime = round(float(Timer)*10)/10.0
    if roundtime != lasttime and broadcast:
	ws.sendMessage(json.dumps(dict(timer=roundtime)))
	lasttime = roundtime
    fill(timescr, " ")
    txtstate = "Time: %s" % Timer
    timescr.addstr(0, 0, txtstate)
    timescr.refresh()

def SetCataTeam(catagory, team):
    statescr = screens['info']
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
    ws.sendMessage(json.dumps(dict(setcatateam=[catagory, team])))
    txtcata = "Catagory: %s" % catagory
    txtteam = "Team: %s" % team
    statescr.addstr(0,0, txtcata)
    statescr.addstr(0,x-60, txtteam)
    statescr.refresh()

def SetLog(Message):
    logscr = screens['log']
    messages.append(Message)
    num=0
    logscr.erase()
    for message in messages[-9:]:
	logscr.addstr(num,0,message)
	num += 1
    logscr.refresh()

def SelectCatagories(window, db):
    contscr = curses.newwin(15,45,10,10)
    contscr.bkgd(' ', curses.color_pair(2))
    contscr.border()
    catagories = db.GetCatagories()
    contscr.addstr(0,15, "Select Catagory")
    count = 0
    catahash = []
    for row in catagories:
        contscr.addstr(3+count,2, "%d - %s " % (1+count, row["title"]))
	catahash.append (dict(title=row["title"], hint=row['hint']))
	count += 1 
    ws.sendMessage(json.dumps(dict(catagories=catahash)))
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

def SelectTeams(window, db):
    contscr = curses.newwin(15,45,10,10)
    contscr.bkgd(' ', curses.color_pair(2))
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

def UpdateTeams(window, db):
    teams = db.GetTeams()
    teamhash = []
    for team in teams:
	teamhash.append (dict(name=team['Name'], score=team['score']))
    ws.sendMessage(json.dumps(dict(scores=teamhash)))

def playFX(fxtype, loop=0):
    ws.sendMessage(json.dumps(dict(playfx=fxtype, loop=loop)))

def playVideo():
    # TODO: Select a video to play
    ws.sendMessage(json.dumps(dict(video="Unitel.mp4")))
