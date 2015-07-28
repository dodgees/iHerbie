#!user/bin/env python

import tweepy
import sqlite3
import datetime
import ConfigParser
import praw
import json


def getKey(item):
    '''Key to allow a list of tweets to be sorted by favorite_count plus retweet_count.'''
    return item.favorite_count + item.retweet_count


def get_tweets(handle, a, t_list, numOfItems=10):
    '''Grabs the tweets from a given list of handles. Default tweets from a handle is 10.'''
    api = a
    for  h in handle:
        user = api.get_user(screen_name=h)

        temp_list = t_list
        for status in tweepy.Cursor(api.user_timeline, user.id, include_entities=True).items(numOfItems):
            temp_list.append(status)

    return temp_list

def getTwitterAPI():
    '''Returns a twitter api object for use grabbing tweets'''
    Config = ConfigParser.ConfigParser()

    Config.read("configFile.ini")

    consumer_key = Config.get('Twitter', 'consumer_key')
    consumer_secret = Config.get('Twitter', 'consumer_secret')

    access_token = Config.get('Twitter', 'access_token')
    access_token_secret = Config.get('Twitter', 'access_token_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def getStatusScreenName(s):
    '''Takes a tweepy status object and returns the screen name associated with that object'''
    status = s
    json_str = json.dumps(status._json)
    parsed_json = json.loads(json_str)
    return parsed_json['user']['screen_name'].encode('utf-8')

#Essentially where the main method would start.
tweets_list = []

## Should create a separate file with getter methods to get these keys. Keep in a gitIgnore file, so it can be stored publicly on github. Check on best practices here.

api = getTwitterAPI()

#Could call this on multiple twitter accounts, just using this method call.
#Could change method to use list of twitter handles and reduce back to one call with multiple handles.
tweets_list = get_tweets(['huskerextra'], api, tweets_list)

tweets_list = sorted(tweets_list, key = getKey, reverse=True)

#Formulat insert statements.
conn = sqlite3.connect('iherbie.db')
curs = conn.cursor()

query = 'INSERT OR REPLACE INTO tweets VALUES(?,?,?,?,?,?,?,?)'

#updated approach to setting tweetVals
for t in tweets_list:
    tweetVals = [str(t.id_str), getStatusScreenName(t), t.text.encode('utf-8'), str("https://twitter.com/statuses/" + t.id_str), int(t.favorite_count), int(t.retweet_count), str(t.created_at), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    curs.execute(query, tweetVals)


conn.commit()

#Execute the rowcount query, use rowcount attribute. If 0, execute insert query
# and use praw to make reddit post.
search_query = '''SELECT COUNT(*) Post_Count FROM posted_tweets
                        where id = ? '''
#We need, 1. id, 2. handle, 3. status, 4. link, 5. favorite_count, 6. retweet_count, 7. date_posted, 8. date_saved
#We have, 1. name, 2. status, 3. Link, 4. favorite_count, 5. Retweet_count, 6. Created_at, 7. Saved at.
postedVals = [str(tweets_list[0].id_str), getStatusScreenName(tweets_list[0]), tweets_list[0].text.encode('utf-8'), str('https://twitter.com/statuses/' + tweets_list[0].id_str), int(tweets_list[0].favorite_count), int(tweets_list[0].retweet_count), str(tweets_list[0].created_at), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

curs.execute(search_query, [postedVals[0]])

posted_tweets_query = 'INSERT INTO posted_tweets VALUES(?,?,?,?,?,?,?, ?)'


#This section needs refractored.
post_count = (curs.fetchone())[0]
if post_count == 0:
    r = praw.Reddit(user_agent='iHerbie script')
    r.login(Config.get('Reddit', 'Username'), Config.get('Reddit', 'Password'))
    tweet_text = str(tweets_list[0].text.encode('utf-8'))
    tweet_url = 'https://twitter.com/statuses/' + str(tweets_list[0].id_str)
    r.submit('huskers', tweet_text, url=tweet_url)
    curs.execute(posted_tweets_query, postedVals)
    print('URL: ' + 'https://twitter.com/statuses/' + str(tweets_list[0].id_str))
else:
    print('Already posted!')
    print('URL: ' + 'https://twitter.com/statuses/' + str(tweets_list[0].id_str))

print(post_count)

conn.commit()
conn.close()
