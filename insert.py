import time,MySQLdb
import random

conn = MySQLdb.connect(host = '127.0.0.1', db = 'test', user = 'root', passwd = '', charset='utf8')

while True:
	content1 = random.randint(0,100)
	content2 = random.randint(0,100)
	cursor = conn.cursor()
	cursor.execute("""
			INSERT INTO testtable 
			(content1, content2)
		VALUES 
			(%s, %s) 
					""", (content1, content2)
					)
	cursor.close()
	conn.commit()
	time.sleep(0.5)
conn.close()

