import sqlite3

conn = sqlite3.connect('iherbie.db')
curs = conn.cursor()


curs.execute('''
	DROP TABLE tweets
	''')

conn.commit()
conn.close()