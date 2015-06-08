#Add tweets table
import sqlite3

conn = sqlite3.connect('iherbie.db')
curs = conn.cursor()


#curs.execute('''
#	DROP TABLE tweets
#	''')

curs.execute('''
CREATE TABLE posted_tweets (
	handle		TEXT,
	status	TEXT,
	link 	TEXT,
	favorite_count	INTEGER,
	retweet_count	INTEGER,
	date_posted	TEXT,
	date_saved 	TEXT,
	PRIMARY KEY (handle, status, date_posted)
	)
	'''	)

conn.commit()
conn.close()