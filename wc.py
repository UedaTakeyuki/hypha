#-*- coding:utf-8 -*-

#from websocket import create_connection
import websocket
import sys
import ssl

#コネクションを張る
#ws = create_connection("wss://titurel.uedasoft.com:8888/websocket")
ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect("wss://titurel.uedasoft.com:8888/websocket")
 
#メッセージを送信
ws.send('hello world!')

#受信したメッセージを表示
print ws.recv()
 
#コネクションを切断
ws.close()
