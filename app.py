from flask import *
import pyrebase

import utils

config = {
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "projectId": "",
  "storageBucket": "",
  "messagingSenderId": "",
  "appId": ""
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
        "tweetID": tweetID,
        "createdAt": tweetData["data"]["created_at"],
        "lang": tweetData["data"]["lang"],
        "author": tweetAuthor,
        "quoteCount": tweetData["data"]["quote_count"],
        "replyCount": tweetData["data"]["reply_count"],
        "retweetCount": tweetData["data"]["retweet_count"],
        "analisis": analisis,
    }
    db.child("tweets").push(tweetData)
    return "OK"

if __name__ == '__main__':
    app.run(debug=True)
