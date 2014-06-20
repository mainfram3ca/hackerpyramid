from ws4py.client.threadedclient import WebSocketClient

class EchoClient(WebSocketClient):
    def sendMessage(self, message):
	self.send(message)

#    def opened(self):
#        def data_provider():
#            for i in range(1, 200, 25):
#                yield "#" * i
                
#        self.send(data_provider())

#        for i in range(0, 200, 25):
#            print(i)
#            self.send("*" * i)

    def closed(self, code, reason):
        print(("Closed down", code, reason))

    def received_message(self, m):
	pass
#        print("=> %d %s" % (len(m), str(m)))

if __name__ == '__main__':
    try:
        ws = EchoClient('ws://localhost:9000/ws', protocols=['http-only', 'chat'])
        ws.daemon = False
        ws.connect()
    except KeyboardInterrupt:
        ws.close()