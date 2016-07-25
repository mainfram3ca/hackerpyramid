from ws4py.client.threadedclient import WebSocketClient
from helper import *
import json

class EchoClient(WebSocketClient):
    def sendMessage(self, message):
	self.send(json.dumps(message))

    def closed(self, code, reason):
        print(("Closed down", code, reason))

    def received_message(self, m):
	try:
	    message = json.loads(str(m))
	    if 'timecode' in message.keys() and message['timecode'] != None and (GetState() == 1 or GetState() == 4 or GetState() == 5): 
		SetTime(float(message['timecode']), False)
	    elif 'videoended' in message.keys():
		SetLog("Video Ended")
		state = GetState()
		#SetState(0)
		if state != 5:
		    SetState(1,False)
		    PlayVideoB()
	    elif 'newclient' in message.keys():
		print "New Client"
		UpdateTeams()
	except:
	    pass

if __name__ == '__main__':
    try:
        ws = EchoClient('ws://localhost:9000/ws', protocols=['http-only', 'chat'])
        ws.daemon = False
        ws.connect()
    except KeyboardInterrupt:
        ws.close()
