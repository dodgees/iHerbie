#!user/bin/env python

import tweepy
import re
import os.path
import sqlite3
import datetime

#import sys
#sys.path.append('C:\Users\dodge_000\Desktop\iHerbieScripts')

## Key to allow a list of tweets to be sorted by favorite_count + retweet_count.
def getKey(item):
	return item.favorite_count + item.retweet_count


## Used to extract a link from a tweet. Will probably be removed --5/19
def extract_link(text):
	#Need to exclude hashtags.
	regex = r'https?://[^\<>"]+|www\.[^\s<>"]+'
	match = re.search(regex, text)
	if match:
		t = match.group()
		t = t.split('#')
		return t[0]
	return ''


## Grabs the tweets from a given handle. Default tweets from a handle is 10.
def get_tweets(handle, a, t_list, numOfItems=10):
	api = a
	user = api.get_user(screen_name=handle)

	temp_list = t_list
	for status in tweepy.Cursor(api.user_timeline, user.id, include_entities=True).items(numOfItems):
		temp_list.append(status)

	return temp_list

#Function: check_tweet. Params: tweet. Return boolean value to indicate if the tweet should be posted.
#This function takes a tweet and checks that the tweet has enough favorites and retweets, was posted on the same day and has a url.

fileName = 'iHerbiePosts.txt'
postFileName = 'iHerbieUrlPosts.txt'
tweets_list = []

## Should create a separate file with getter methods to get these keys. Keep in a gitIgnore file, so it can be stored publicly on github. Check on best practices here.
consumer_key = 'GVhC6Y6131iTYistRrKtXKNOV'
consumer_secret = 'bDf5K7TeGKNWZmmIpxj3WPK5GZO1rLzM6CEMcDdNBlaEtHTRjd'

access_token = '237425894-ZOQ9y2bgvKpNDiJrVY0iXFZiMe3AXuxm1P4AXVrH'
access_token_secret = '8MPtV4M28FvgLIyC6Pvi1DVcXjbAQgzlyUT48g7vO4ohj'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

tweets_list = get_tweets('huskerextra', api, tweets_list)

tweets_list = sorted(tweets_list, key = getKey, reverse=True)

for t in tweets_list:
	print t.text.encode('utf-8')
	print t.created_at
	print t.entities
	print (t.favorite_count + t.retweet_count)
	print '\n'

if not os.path.isfile(fileName):
	f = open(fileName, 'w')
	f.write(tweets_list[0].text.encode('utf-8'))
	f.close()
else:
	f = open(fileName, 'r')
	line = f.readline()
	f.close()

	if line == tweets_list[0].text.encode('utf-8'):
		print 'This comparison works'
	else:
		print 'The comparison failed'
		print line

#print tweets_list[0].text.encode('utf-8')

#Code to post and check tweet using files.

if os.path.isfile(fileName):
	f = open(fileName, 'r')
	lines = f.readlines()
	f.close()

	newPost = False #True changed to ignore file processing.

	for l in lines:
		if l == tweets_list[0].text.encode('utf-8'):
			newPost = False

	if newPost:
		UrlFile = open(postFileName, 'a+')
		try:
			UrlFile.write(tweets_list[0].entities['urls'][0]['expanded_url'])
		except Exception, e:
			raise e
		finally:
			UrlFile.close()

#print tweets_list[0].url
##public_tweets = api.home_timeline()
##for tweet in public_tweets:
##	print tweet.text.encode('utf-8')

user = api.get_user(screen_name='huskerextra')



#Formulat insert statements.
conn = sqlite3.connect('iherbie.db')
curs = conn.cursor()

query = 'INSERT OR REPLACE INTO tweets VALUES(?,?,?,?,?,?,?)'

for status in tweepy.Cursor(api.user_timeline, user.id).items(10):
	vals = [repr(str(user.name.encode('utf-8'))), repr(str(status.text.encode('utf-8'))), repr(str(extract_link(status.text.encode('utf-8')))), int(status.favorite_count), int(status.retweet_count), repr(str(status.created_at)), repr(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))]
	
	print status.text.encode('utf-8')
	print status.created_at
	print status.favorite_count
	print status.retweet_count
	print status.source
	print extract_link(status.text.encode('utf-8'))
	print '\n\n\n'
	print query
	print vals
	print '\n\n\n'

	curs.execute(query, vals)

conn.commit()

#Execute the rowcount query, use rowcount attribute. If 0, execute insert query
# and use praw to make reddit post.
search_query = '''SELECT COUNT(*) Post_Count FROM posted_tweets 
						where handle = ? 
						and status = ?
						and date_posted = ? '''


vals = [repr(str(user.name.encode('utf-8'))), repr(str(tweets_list[0].text.encode('utf-8'))), repr(str(extract_link(tweets_list[0].text.encode('utf-8')))), int(tweets_list[0].favorite_count), int(tweets_list[0].retweet_count), repr(str(tweets_list[0].created_at)), repr(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))]

curs.execute(search_query, [vals[0], vals[1], vals[5]])

posted_tweets_query = 'INSERT INTO posted_tweets VALUES(?,?,?,?,?,?,?)'

post_count = (curs.fetchone())[0]
if post_count == 0:
	curs.execute(posted_tweets_query, vals)
else:
	print 'Already posted!'


print post_count

conn.commit()
conn.close()
