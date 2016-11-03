# -*- coding: utf-8 -*-
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from pymongo import MongoClient

ckey = 'yiP3jGov2bpJxBbSNcuCFjdV4'
csecret = 'FB22w1rwgL3hOqk65TzVgWvHH69FFAVrGiurC3BuZebTKLz8zw'
atoken = '158405714-DvDQyFCplHlIU6pAkvFh4cK23AKTDzHI7H2KBuq3'
asecret = 'VqHX36UZoQvC2kADqnYoDmz7TC2jlfK2ubnwn3Cgprgzh'

# Mine the tweets and load the data to Mongo DB
class listener(StreamListener):
    def on_data(self, data):
        try:
            with open('twittertweets.json', 'a') as f:
                f.write(data)
                tweet = json.loads(data)
                print tweet
                client = MongoClient('localhost', 27017)
                db = client['twitter']
                collection = db['tweets']
                collection.insert(tweet)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track = ['diabetes',' HbA1c ',' FPG ',' OGTT ',' A1c ',' A1C ',' IFG ',' IGT ',' FBG ',' FBS ',' eAG ',' DMT2 ',' T2DM ',' impaired fasting glucose ',' impaired glucose tolerance ',' blood glucose ',' FBS sugar ',' estimate average glucose '],languages=['en'])

