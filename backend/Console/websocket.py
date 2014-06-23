from ws4py.client.threadedclient import WebSocketClient
from helper import *
import json

class EchoClient(WebSocketClient):
    def sendMessage(self, message):
	self.send(json.dumps(message))

    def closed(self, code, reason):
        print(("Closed down", code, reason))

    def received_message(self, m):
	message = json.loads(str(m))
	if 'timecode' in message.keys() and message['timecode'] != None and GetState() == 1:
	    SetTime(float(message['timecode']), False)

if __name__ == '__main__':
    try:
        ws = EchoClient('ws://localhost:9000/ws', protocols=['http-only', 'chat'])
        ws.daemon = False
        ws.connect()
    except KeyboardInterrupt:
        ws.close()