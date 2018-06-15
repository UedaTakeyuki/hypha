#-*- coding:utf-8 -*-

#from websocket import create_connection
import tornado.ioloop
import websocket
import sys
import ssl
from tornado.options import define, options
import json
import piserialnumber

commands = {
  "register": json.dumps({"command": "register", "id": piserialnumber.serial()})	
}
print(commands["register"])

if __name__ == "__main__":

	# command options
	define("protocol", default="wss:", help="ws: or wss:(default)")
	define("url", default="//titurel.uedasoft.com:8888/websocket", help="url string without protocol like //aaa.bbb.ccc/ddd")
	define("config_file", default="", help="config file path")
	options.parse_command_line()

	if options.config_file:
		options.parse_config_file(options.config_file)

	if options.protocol == "ws:":
		#ws = create_connection("wss://titurel.uedasoft.com:8888/websocket")
		ws = websocket.WebSocket()
 	else:
		ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})

	ws.connect(options.protocol + options.url)

	#メッセージを送信
	ws.send(commands["register"])

	while True:
		#受信したメッセージを表示
		print ws.recv()
 
	#コネクションを切断
	#ws.close()
#	tornado.ioloop.IOLoop.instance().start()
