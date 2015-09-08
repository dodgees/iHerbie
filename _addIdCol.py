import sqlite3

conn = sqlite3.connect('iherbie.db')
curs = conn.cursor()

curs.execute('''
ALTER TABLE TWEETS ADD COLUMN twitter_id TEXT;
             ''')

conn.commit()
conn.close()
