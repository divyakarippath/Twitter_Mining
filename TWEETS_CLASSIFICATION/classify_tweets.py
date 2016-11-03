import pickle
from pymongo import MongoClient
import csv
import sys

# set encoding
reload(sys)
sys.setdefaultencoding('utf8')


def createCSVHeader(csvWriter_p, csvWriter_ad):
    headerLine1 = ['CREATED TIME', 'TWEET ID', 'USER ID', 'NAME', 'SCREEN NAME', 'LOCATION', 'FOLLOWERS', 'FRIENDS','FOLLOWING', 'TWEET MESSAGE', 'RETWEETS', 'RETWEETED']
    headerLine2 = ['', '', '', '', '', '', '', '', '', '', '', '']
    csvWriter_p.writerow(headerLine1)
    csvWriter_p.writerow(headerLine2)
    csvWriter_ad.writerow(headerLine1)
    csvWriter_ad.writerow(headerLine2)


def loadClassifier():
    classifier_file = open("naiveBayes.pickle", "rb")
    return pickle.load(classifier_file)


def load_data_fromDB(db):
    return db.tweets.find()


def getAllDictionary(words):
    return dict([(word, True) for word in words])


def updateCSVFile(csvWriter, data):
    csvWriter.writerow([data['created_at'], data['id'], data['user']['id'], data['user']['name'], data['user']['screen_name'],data['user']['location'], data['user']['followers_count'],data['user']['friends_count'], data['user']['following'], data['text'], data['retweet_count'],
        data['retweeted']])


# Open csv files and create the headers
csvWriter_p = csv.writer(open('Personal_Tweets.csv', mode='w'))
csvWriter_ad = csv.writer(open('Ad_Tweets.csv', mode='w'))
createCSVHeader(csvWriter_p, csvWriter_ad)

# Load the classifier from pickle
classifier = loadClassifier()

# initialize mongo client and load data from Mongo Db
client = MongoClient()
db = client['twitter']
cursor = load_data_fromDB(db)

for data in cursor:
    if data.has_key('text'):
        tweet = data['text']
        test_data = getAllDictionary(tweet.split())
        result = classifier.classify(test_data)
        if result == 'personal':
            db.personal_tweets.insert(data)
            updateCSVFile(csvWriter_p, data)
        
        else:
            db.ad_tweets.insert(data)
            updateCSVFile(csvWriter_ad, data)

    else:
        continue
