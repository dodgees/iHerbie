import sqlite3

conn = sqlite3.connect('iherbie.db')
curs = conn.cursor()


curs.execute('''
SELECT * FROM tweets
	'''	)
names = [f[0] for f in curs.description]

for row in curs.fetchall():
	for pair in zip(names, row):
		print '%s: %s' % pair
	
	print

print names

conn.commit()
conn.close()