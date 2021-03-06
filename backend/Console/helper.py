import curses, time, datetime, database, logging
from interval import setInterval
import curses.textpad

states = ["Showing Penny", "Showing Video", "Showing Catagories", "Round Running", "Select Team", "Stopping Videos"]
state = 0
messages = []
screens = {}
lasttime = 0
runtime = 0
logging.basicConfig(filename='Pyramid.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
updatetimer = True

def setws(rws, rdb, rbuzz, rcataclass):
	global ws, db, buzz, cataclass
	ws = rws
	db = rdb
	buzz = rbuzz
	cataclass = rcataclass

def setscreens(window, top, time, log, info, teams, runtime):
	screens['window'] = window
	screens['top'] = top
	screens['time'] = time
	screens['log'] = log
	screens['info'] = info
	screens['teams'] = teams
	screens['runtime'] = runtime

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

def SendAlert(m=""):
	global updatetimer
	updatetimer = False
	win = curses.newwin(1, 60, 12, 10)
	win.bkgd(' ', curses.color_pair(2))
	if m == "":
		tb = curses.textpad.Textbox(win)
		text = tb.edit()
		if text != "":
			ws.sendMessage(dict(message=text,name="console"))
		updatetimer = True
		del win
		screens['window'].touchwin()
		screens['window'].refresh()
		SetLog(text)
	else:
		text = m
		if text != "":
			ws.sendMessage(dict(message=text,name="console"))
		updatetimer = True
		

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
	if catagory == None:
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

def SetAnswer():
	Answer = cataclass.GetAnswer()
	if Answer == None:
		return None
	ws.sendMessage(dict(word=Answer,catagory=cataclass.GetCatagory()['Title']))
	return Answer

def SetLog(Message, LogOnly=False):
	logging.info(Message)
	if LogOnly == False: 
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
	contscr = curses.newwin(15,45,10,1)
	contscr.bkgd(' ', curses.color_pair(2))
	contscr.border()
	catagories = cataclass.GetCatagories(team)
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
	if result != False:
		cataclass.SetCatagory(result)
	return result

def SelectTeams(window):
	contscr = curses.newwin(25,45,10,10)
	contscr.bkgd(' ', curses.color_pair(2))
	contscr.border()
	teams = db.GetTeams()
	contscr.addstr(0,15, "Select Team")
	count = 1

	for row in teams:
		if count <= 9:
			contscr.addstr(3+count,2, "%d - %s " % (count, row["Name"]))
		else:
			contscr.addstr(3+count,2, "%s - %s " % (chr(count+87), row["Name"]))
		count += 1 

	contscr.addstr(22,2, "(Q)uit without Selecting")
	contscr.addstr(23,2, "Select:")
	contscr.refresh()

	while 1:
		c = contscr.getch()
		if c == ord('q'):
			result = False
			break
		#if c >= 48 and c <= 57:
		if c >= 49 and c <= 57:
			try:
				result = teams[c-49]
				break
			except IndexError:
				pass
		if c >= 65 and c <= 90:
			try:
				result = teams[c-67]
				break
			except IndexError:
				pass
		if c >= 97 and c <= 122:
			try:
				#results = teams[c-99]
				result = teams[c-97+9]
				break
			except IndexError:
				pass
 
	del contscr
	window.touchwin()
	window.refresh()
	return result

def UpdateScores():
	scrteams = screens['teams']
	ldb = database.pyrDB()
	teams = ldb.GetTeams()
	ldb.close()
	teamhash = []
	scrteams.border()
	scrteams.addstr(0,15, "Teams")

	count=0

	for team in teams:
	
		if team['score'] == None:
			score = 0
		else:
			score = team['score']

		teamhash.append (dict(name=team['Name'],score=score))
		scrteams.addstr(2+count,2, "%s: %d" % (team["Name"], score))
		count += 1

	scrteams.refresh()

	return teamhash

def UpdateTeams():
	ldb = database.pyrDB()
	teams = ldb.GetTeams()
	ldb.close()
	teamhash = []
	screens['teams'].clear()
	screens['teams'].border()
	screens['teams'].addstr(0,15, "Teams")

	count=0
	for team in teams:
	
		if team['score'] == None:
			score = 0
		else:
			score=team['score']
		teamhash.append (dict(name=team['Name'], score=score, celeb_name=team['celeb_name'], celeb_bio=team['celeb_bio'], partner_name=team['partner_name'], partner_bio=team['partner_bio']))
		screens['teams'].addstr(2+count,2, "%s: %d" % (team["Name"], team["score"]))
		count += 1

	ws.sendMessage(dict(teams=teamhash))

	screens['teams'].refresh()

def playFX(fxtype, loop=0):
	ws.sendMessage(dict(playfx=fxtype, loop=loop))

def playCredits():
	SetLog("Playing End Credits")
	ws.sendMessage(dict(message="Playing End Credits",name="console"))
	ws.sendMessage(dict(endcredits="play"))

def playVideo():
	ldb = database.pyrDB()
	v = ldb.GetNextVideo()
	if (v == None):
		SetLog("NO VIDEOS IN THE DATABASE! DID YOU INIT?")
	else:
		SetLog("Playing: " + v)
		ws.sendMessage(dict(message="Playing %s"%v,name="console"))
		ws.sendMessage(dict(video=v))

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

def StartRunTime():
	global runtime
	if (runtime == 0):
		runtime = int(time.time())
	else:
		runtime = 0

@setInterval(1)
def RunTimer():
	lruntime = int(time.time()) - runtime
	if (runtime == 0):
		rtime = str(datetime.timedelta(seconds=0))
	else:
		rtime = str(datetime.timedelta(seconds=lruntime))
	scores = UpdateScores()

	if (state != 3 and updatetimer):
		ltimescr = screens['runtime']
		fill(ltimescr, " ")
		txtstate = "Run Time: %s" % rtime
		ltimescr.addstr(0, 0, txtstate)
		ltimescr.refresh()

	ws.sendMessage(dict(runtime=rtime, scores=scores))

