import sqlite3

conn = sqlite3.connect('iherbie.db')
curs = conn.cursor()


#curs.execute('''
#	DROP TABLE tweets
#	''')

curs.execute('''
CREATE TABLE tweets (
	handle		TEXT,
	status	TEXT,
	link 	TEXT,
	favorite_count	INTEGER,
	retweet_count	INTEGER,
	date_posted	TEXT PRIMARY KEY,
	date_saved 	TEXT
	)
	'''	)

conn.commit()
conn.close()