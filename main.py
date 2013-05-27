# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.websocket
import torndb
import json
import datetime
import threading

class DateTimeEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return obj.isoformat()
		elif isinstance(obj, datetime.date):
			return obj.isoformat()
		elif isinstance(obj, datetime.timedelta):
			return (datetime.datetime.min + obj).time().isoformat()
		else:
			return super(DateTimeEncoder, self).default(obj)

# 以上对datetime进行格式化

class SocketHandler(tornado.websocket.WebSocketHandler):
	clients = set()
	
	@staticmethod
	def send_to_all(message):
		for c in SocketHandler.clients:
			c.write_message(message)

	def open(self):	
		print 'Connect'
		self.write_message(jsn)
		SocketHandler.clients.add(self)
#		tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1), self.test())

	def on_close(self):
		print 'Disconnect'
		SocketHandler.clients.remove(self)

	def on_message(self, message):
		SocketHandler.send_to_all(jsn)

#	def test(self):
#		self.write_message(jsn)

# 以上WebSocket打开以及记录客户端的连接

class Index(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

db = torndb.Connection(host = '127.0.0.1', database = 'test', user = 'root', password = None, max_idle_time = 7)
# 连接数据库
#data = db.query("select * from testtable order by id desc LIMIT 3")
# 读数据
#jsn= DateTimeEncoder().encode(data)


def readdb():
	data = db.query("select * from testtable order by id desc LIMIT 21")
	global jsn 
	jsn = DateTimeEncoder().encode(data)
#	print jsn
	db.reconnect()
	global t #Notice: use global variable!
	t = threading.Timer(0.1, readdb)
	t.start()

readdb()


if __name__ == '__main__':
	app = tornado.web.Application([
		('/', Index),
		('/soc', SocketHandler),
	])
	app.listen(8000)
	tornado.ioloop.IOLoop.instance().start()
