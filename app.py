from flask import *
import pyrebase
import os
from dotenv import load_dotenv

import utils

load_dotenv()

config = {
  "apiKey": os.environ['API_KEY'],
  "authDomain": os.environ['AUTH_DOMAIN'],
  "databaseURL": os.environ['DATABASE_URL'],
  "projectId": os.environ['PROJECT_ID'],
  "storageBucket": os.environ['STORAGE_BUCKET'],
  "messagingSenderId": os.environ['MESSAGING_SENDER_ID'],
  "appId": os.environ['APP_ID']
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)

@app.route('/pushUserToDB', methods=["POST"])
def pushUserToDB():
    uid = request.json["uid"]
    userData = {
    "firstName": request.json["firstName"],
    "lastName": request.json["lastName"],
    "email": request.json["email"],
    }
    db.child("users").child(uid).set(userData)
    return "OK"

@app.route('/pushTweetAnalisisToDB', methods=["POST"])
def pushTweetAnalisisToDB():
    url = request.json["url"]
    tweetID = utils.getTweetID(url)
    tweetAuthor = utils.getTweetAuthor(url)
    tweetData = utils.getTweetData(tweetID)
    tweetText = utils.cleanText(tweetData["data"]["full_text"])
    analisis = utils.analyzeTweet(tweetText)
    tweetData = {
        "url": url,
        "createdAt": tweetData["data"]["created_at"],
        "lang": tweetData["data"]["lang"],
        "author": tweetAuthor,
        "quoteCount": tweetData["data"]["quote_count"],
        "replyCount": tweetData["data"]["reply_count"],
        "retweetCount": tweetData["data"]["retweet_count"],
        "analisis": analisis,
    }
    db.child("tweets").child(tweetID).set(tweetData)
    return tweetID

if __name__ == '__main__':
    app.run(debug=True)
