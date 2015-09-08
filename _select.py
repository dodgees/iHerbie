import sqlite3
import datetime

conn = sqlite3.connect('iherbie.db')
curs = conn.cursor()

vals = [str(datetime.date.today().strftime("%Y-%m-%d %H:%M:%S"))]

search_query = "SELECT * FROM tweets order by date_posted desc, (favorite_count + retweet_count) desc"

#curs.execute('''
#SELECT * FROM tweets order by date_posted desc, (favorite_count + retweet_count) desc
#    ''' )

curs.execute(search_query)


names = [f[0] for f in curs.description]


for row in curs.fetchall():
	for pair in zip(names, row):
		print('%s: %s' % pair)

	print()

#print names
#print curs.fetchall()

conn.commit()
conn.close()
