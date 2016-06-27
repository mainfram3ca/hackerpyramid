from random import randrange

class catagories:
	def __init__(self, db):
		self.db = db
		self.catagory = None

	def GetCatagories(self, team):
		self.catagories = self.db.GetCatagories(team)
		return self.catagories

	def SetCatagory(self, catagory):
		self.catagory = catagory
		# Setup the answers
		self.avail = catagory['Answers'].split(',')
		self.correct = []
		self.passed = []
		self.buzzed = []
		self.SelectAnswer()

	def Judged(self, result):
		if result == 1:
		    # Judges Accepted
		    self.correct.append(self.avail[self.selected])
		    del self.avail[self.selected]
		elif result == 2:
		    # Judges Passed
		    self.passed.append(self.avail[self.selected])
		    del self.avail[self.selected]
		    pass
		elif result == 3:
		    #Judges Buzzed
		    self.buzzed.append(self.avail[self.selected])
		    del self.avail[self.selected]
		    pass
		self.SelectAnswer()

	def SelectAnswer(self):
		# Select the Answer
		if len(self.avail) == 0:
		    if len(self.passed) == 0:
			self.selected = None
			return
		    else:
			self.avail = self.passed
			self.passed = []
		self.selected = randrange(0,len(self.avail))

	def GetCatagory(self):
		return self.catagory

	def UseCatagory(self):
		self.db.UseCatagory(self.catagory['id'])

	def GetAnswer(self):
		if self.selected == None:
			return None
		else:
			return self.avail[self.selected]
	
	def Clear(self):
		self.catagory = None

