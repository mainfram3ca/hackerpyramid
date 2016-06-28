#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import random
import os
import json

import cherrypy

from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage


class ChatWebSocketHandler(WebSocket):
	def received_message(self, m):
		print m
		# Try parsing the data as JSON, if it fails, don't bother sending it out.
		try:
			message = json.loads(str(m))
			cherrypy.engine.publish('websocket-broadcast', m)
		except:
			print "Non JSON frame received"
			pass

	def closed(self, code, reason="A client left the room without a proper explanation."):
		cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))

class Root(object):
	def __init__(self, host, port, ssl=False):
		self.host = host
		self.port = port
		self.scheme = 'wss' if ssl else 'ws'

	@cherrypy.expose
	def ws(self):
		cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

if __name__ == '__main__':
	import logging
	from ws4py import configure_logger
	configure_logger(level=logging.DEBUG)

	parser = argparse.ArgumentParser(description='Echo CherryPy Server')
	parser.add_argument('--host', default='0.0.0.0')
	parser.add_argument('-p', '--port', default=9000, type=int)
	parser.add_argument('--ssl', action='store_true')
	parser.add_argument('-r', '--rootdir', required=True, help='The absolute path to the "Audience" directory')
	args = parser.parse_args()

	cherrypy.config.update({'server.socket_host': args.host,
				'server.socket_port': args.port,
				'tools.staticdir.root': args.rootdir })

	if args.ssl:
		cherrypy.config.update({'server.ssl_certificate': './server.crt',
					'server.ssl_private_key': './server.key'})

	WebSocketPlugin(cherrypy.engine).subscribe()
	cherrypy.tools.websocket = WebSocketTool()

	cherrypy.quickstart(Root(args.host, args.port, args.ssl), '', config={
		'/ws': {
			'tools.websocket.on': True,
			'tools.websocket.handler_cls': ChatWebSocketHandler
			}
		,
		'/': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': ''
			}
		}
	)
