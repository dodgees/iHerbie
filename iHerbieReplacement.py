#!user/bin/env python

import tweepy
import re
import os.path
import sqlite3
import datetime

## Key to allow a list of tweets to be sorted by favorite_count + retweet_count.
def getKey(item):
    return item.favorite_count + item.retweet_count

## Grabs the tweets from a given handle. Default tweets from a handle is 10.
def get_tweets(handle, a, t_list, numOfItems=10):
    api = a
    user = api.get_user(screen_name=handle)

    temp_list = t_list
    for status in tweepy.Cursor(api.user_timeline, user.id, include_entities=True).items(numOfItems):
        temp_list.append(status)

    return temp_list

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

user = api.get_user(screen_name='huskerextra')



#Formulat insert statements.
conn = sqlite3.connect('iherbie.db')
curs = conn.cursor()

query = 'INSERT OR REPLACE INTO tweets VALUES(?,?,?,?,?,?,?,?)'

for status in tweepy.Cursor(api.user_timeline, user.id).items(10):
    tweetVals = [str(status.id_str), repr(str(user.name.encode('utf-8'))), repr(str(status.text.encode('utf-8'))), repr("https://twitter.com/statuses/" + status.id_str), int(status.favorite_count), int(status.retweet_count), repr(str(status.created_at)), repr(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))]
    curs.execute(query, tweetVals)

conn.commit()

#Execute the rowcount query, use rowcount attribute. If 0, execute insert query
# and use praw to make reddit post.
search_query = '''SELECT COUNT(*) Post_Count FROM posted_tweets
                        where id = ? '''
#We need, 1. id, 2. handle, 3. status, 4. link, 5. favorite_count, 6. retweet_count, 7. date_posted, 8. date_saved
#We have, 1. name, 2. status, 3. Link, 4. favorite_count, 5. Retweet_count, 6. Created_at, 7. Saved at.
postedVals = [str(tweets_list[0].id_str), repr(str(user.name.encode('utf-8'))), repr(str(tweets_list[0].text.encode('utf-8'))), 'https://twitter.com/statuses/' + str(tweets_list[0].id_str), int(tweets_list[0].favorite_count), int(tweets_list[0].retweet_count), repr(str(tweets_list[0].created_at)), repr(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))]


print(len(postedVals))
curs.execute(search_query, [postedVals[0]])

posted_tweets_query = 'INSERT INTO posted_tweets VALUES(?,?,?,?,?,?,?, ?)'


#This section needs refractored.
#Create method to decide if a new tweet should be posted.
#Use select query. Check posts from current date with above 5 popularity.
#Need to iterate through days post, stop when one is found. Only select posts with date posted > current date.

post_count = (curs.fetchone())[0]
if post_count == 0:
    curs.execute(posted_tweets_query, postedVals)
    print('URL: ' + 'https://twitter.com/statuses/' + str(tweets_list[0].id_str))
else:
    print('Already posted!')
    print('URL: ' + 'https://twitter.com/statuses/' + str(tweets_list[0].id_str))

print(post_count)

conn.commit()
conn.close()
