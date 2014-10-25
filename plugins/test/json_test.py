import socket
import json

data = {'module': "firewall", 'data': {"port": "1234", "host": "192.168.1.1", "time": "5", "action": "block"}}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 1337))
s.send(json.dumps(data))
s.close()
