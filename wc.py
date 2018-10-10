#-*- coding:utf-8 -*-

#from websocket import create_connection
import os
import tornado.ioloop
import websocket
import sys
import ssl
from tornado.options import define, options
import json
import piserialnumber
import subprocess32 as subprocess
import traceback
import logging

if not os.path.exists('/var/log/SCRIPT/'):
	os.makedirs('/var/log/SCRIPT/')
logging.basicConfig(format='%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s',filename='/var/log/SCRIPT/hypha.log',level=logging.DEBUG)

commands = {
  "register": json.dumps({"command": "register", "id": piserialnumber.serial()})	
}

if __name__ == "__main__":

	# command options
	define("protocol", default="wss:", help="ws: or wss:(default)")
	define("url", default="//titurel.uedasoft.com:8888/websocket", help="url string without protocol like //aaa.bbb.ccc/ddd")
	define("config_file", default="", help="config file path")
	define("device_id",	default="", help="specific device id in case. without this option, device original id (cpu id, eth mac address, etc) is used.")
	options.parse_command_line()

	if options.config_file:
		options.parse_config_file(options.config_file)

	if options.protocol == "ws:":
		#ws = create_connection("wss://titurel.uedasoft.com:8888/websocket")
		ws = websocket.WebSocket()
 	else:
		ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})

	if options.device_id:
		device_id = options.device_id
	else:
		device_id = piserialnumber.serial()

#	ws.connect(options.protocol + options.url)
	ws.connect(options.protocol + options.url, 
		   header=["x-custome-id: {}".format(device_id),
			   "Authorization: Bearer 0000"
			  ])

	#メッセージを送信
	ws.send(commands["register"])

	while True:
		#受信したメッセージを表示
		recv_str = ws.recv()
		print recv_str
		try:
			logging.info("ws.recv() = {}".format(recv_str))
			ms = json.loads(recv_str)
			if ms["order"] == "exec_bash":
				print ("exec {}".format(ms["cmd_str"]))
				logging.info("exec {}".format(ms["cmd_str"]))

				p = subprocess.Popen(ms["cmd_str"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				std_out, std_err = p.communicate(None, timeout=60)
				result = std_out.strip()
				error  = std_err.strip()

				logging.info("result = {}".format(result))
				logging.info("error = {}".format(error))

				result_json = json.dumps({
					"order" : "response",
					"result": result,
					"error" : error
				})
				logging.info("result_json = {}".format(result_json))
				
				ws.send(result_json)
		except:
			info=sys.exc_info()
			print (traceback.format_exc(info[0]))
			pass
 
	#コネクションを切断
	#ws.close()
#	tornado.ioloop.IOLoop.instance().start()
