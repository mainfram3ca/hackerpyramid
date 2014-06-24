import curses, time, datetime

states = ["Showing Penny", "Showing Video", "Showing Catagories", "Round Running", "Select Team", "Stopping Videos"]
state = 0
messages = []
screens = {}
lasttime = 0

def setws(rws):
    global ws
    ws = rws

def setscreens(window, top, time, log, info, teams):
    screens['window'] = window
    screens['top'] = top
    screens['time'] = time
    screens['log'] = log
    screens['info'] = info
    screens['teams'] = teams

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
    global state
    state = State
    topscr = screens['top']
    if broadcast:
	ws.sendMessage(dict(state=State))
    fill(topscr, " ")
    txtstate = "State: %s" % states[State]
    topscr.addstr(0, 0, txtstate)
    topscr.refresh()

def GetState():
    return state

def SetTime(Timer, broadcast=True):
    global lasttime
    timescr = screens['time']
    roundtime = round(float(Timer)*10)/10.0
    if roundtime != lasttime and broadcast:
	ws.sendMessage(dict(timer=roundtime))
	lasttime = roundtime
    fill(timescr, " ")
    txtstate = "Time: %s" % Timer
    timescr.addstr(0, 0, txtstate)
    timescr.refresh()

def SetCataTeam(catagory, team):
    infoscr = screens['info']
    y, x = infoscr.getmaxyx()
    fill(infoscr, " ")
    if catagory == False:
	catagory = ""
    else:
	catagory = catagory['Title']
    if team == False:
	team = ""
    else:
	team = team['Name']
    ws.sendMessage(dict(setcatateam=[catagory, team]))
    txtcata = "Catagory: %s" % catagory
    txtteam = "Team: %s" % team
    infoscr.addstr(0,0, txtcata)
    infoscr.addstr(0,x-60, txtteam)
    infoscr.refresh()

def SetLog(Message):
    logscr = screens['log']
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messages.append("%s: %s" %(timestamp, Message))
    num=1
    logscr.erase()
    logscr.border()
    for message in messages[-9:]:
	logscr.addstr(num,1,message)
	num += 1
    logscr.refresh()

def ShowError(Error):
    SetLog("ERROR: %s" % Error)

def SelectCatagories(db, team):
    contscr = curses.newwin(15,45,10,10)
    contscr.bkgd(' ', curses.color_pair(2))
    contscr.border()
    catagories = db.GetCatagories(team)
    contscr.addstr(0,15, "Select Catagory")
    count = 0
    catahash = []
    for row in catagories:
        contscr.addstr(3+count,2, "%d - %s " % (1+count, row["title"]))
	catahash.append (dict(title=row["title"], hint=row['hint']))
	count += 1 
    ws.sendMessage(dict(catagories=catahash))
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
    screens['window'].touchwin()
    screens['window'].refresh()
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

def UpdateTeams(db):
    teams = db.GetTeams()
    teamhash = []
    screens['teams'].clear()
    screens['teams'].border()
    screens['teams'].addstr(0,15, "Teams")

    count=0
    for team in teams:
	
	teamhash.append (dict(
		name=team['Name'], 
		score=team['score'], 
		celeb_name=team['celeb_name'],
		celeb_bio=team['celeb_bio'],
		partner_name=team['partner_name'],
		partner_bio=team['partner_bio'],
	))
        screens['teams'].addstr(2+count,2, "%s: %d" % (team["Name"], team["score"]))
	count += 1

    ws.sendMessage(dict(scores=teamhash))

    screens['teams'].refresh()

def playFX(fxtype, loop=0):
    ws.sendMessage(dict(playfx=fxtype, loop=loop))

def playVideo():
    # TODO: Select a video to play
    ws.sendMessage(dict(video="Unitel.mp4"))

def PlayVideoB():
    # Display a message to warn about playing another video
    window = screens['window']
    y, x = window.getmaxyx()
    contscr = curses.newwin(3,30,int(y/2-2),int(x/2-15))
    contscr.bkgd(' ', curses.color_pair(2))
    contscr.border()
    contscr.addstr(1,8, "Playing Video")
    contscr.refresh()
    time.sleep(5)
    if GetState() != 5:
	SetLog("Playing Another Video")
	playVideo()
    else:
	SetState(0)
	SetLog("Ending Videos")
    del contscr
    window.touchwin()
    window.refresh()

