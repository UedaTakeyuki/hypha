#-*- coding:utf-8 -*-

#from websocket import create_connection
import tornado.ioloop
import websocket
import sys
import ssl
from tornado.options import define, options
import json
import piserialnumber
import subprocess32 as subprocess
import traceback

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
		recv_str = ws.recv()
		print recv_str
		try:
			ms = json.loads(recv_str)
			if ms["order"] == "exec_bash":
				print ("exec {}".format(ms["cmd_str"]))
				p = subprocess.Popen(ms["cmd_str"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				std_out, std_err = p.communicate(None, timeout=30)
				result = std_out.strip()
				error  = std_err.strip()
		except:
			info=sys.exc_info()
			print (traceback.format_exc(info[0]))
			pass
 
	#コネクションを切断
	#ws.close()
#	tornado.ioloop.IOLoop.instance().start()
