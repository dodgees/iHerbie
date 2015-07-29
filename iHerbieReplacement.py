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

def getStatusScreenName(status):
    '''Takes a tweepy status object and returns the screen name associated with that object'''
    s = status
    json_str = json.dumps(s._json)
    parsed_json = json.loads(json_str)
    return parsed_json['user']['screen_name'].encode('utf-8')

def insertTweets(tweetList, connection):
    '''Takes a list of tweets and DB connection to insert tweets into the DB'''
    conn = connection
    curs = conn.cursor()

    tweets_list = tweetList

    query = 'INSERT OR REPLACE INTO tweets VALUES(?,?,?,?,?,?,?,?)'

    #updated approach to setting tweetVals
    for t in tweets_list:
        tweetVals = [str(t.id_str), getStatusScreenName(t), repr(t.text.encode('utf-8')), str("https://twitter.com/statuses/" + t.id_str), int(t.favorite_count), int(t.retweet_count), str(t.created_at), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        curs.execute(query, tweetVals)

    conn.commit()

def main():
    tweets_list = []

    api = getTwitterAPI()

    tweets_list = get_tweets(['huskerextra', 'OWHbigred'], api, tweets_list)

    tweets_list = sorted(tweets_list, key = getKey, reverse=True)

    #Formulat insert statements.
    conn = sqlite3.connect('iherbie.db')
    insertTweets(tweets_list, conn)

    #Execute the rowcount query, use rowcount attribute. If 0, execute insert query
    # and use praw to make reddit post.
    search_query = '''SELECT COUNT(*) Post_Count FROM posted_tweets
                            where id = ? '''

    postedVals = [str(tweets_list[0].id_str), getStatusScreenName(tweets_list[0]), repr(tweets_list[0].text.encode('utf-8')), str('https://twitter.com/statuses/' + tweets_list[0].id_str), int(tweets_list[0].favorite_count), int(tweets_list[0].retweet_count), str(tweets_list[0].created_at), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    curs = conn.cursor()
    curs.execute(search_query, [postedVals[0]])

    posted_tweets_query = 'INSERT INTO posted_tweets VALUES(?,?,?,?,?,?,?,?)'


    #This section needs refractored.
    post_count = (curs.fetchone())[0]
    if post_count == 0:
        Config = ConfigParser.ConfigParser()
        Config.read("configFile.ini")

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

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
