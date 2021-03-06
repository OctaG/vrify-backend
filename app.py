from flask import *
import pyrebase
import os
from dotenv import load_dotenv
from datetime import date

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

@app.route('/pushTweetAnalysisToDB', methods=["POST"])
def pushTweetAnalysisToDB():
    url = request.json["url"]
    tweetID = utils.getTweetID(url)
    tweetAuthor = utils.getTweetAuthor(url)
    tweetData = utils.getTweetData(tweetID)
    tweetText = utils.cleanText(tweetData["data"]["full_text"])
    analysis = utils.analyzeTweet(tweetText)
    tweetData = {
        "url": url,
        "tweetID": tweetID,
        "lastAnalysis": str(date.today()),
        "createdAt": tweetData["data"]["created_at"],
        "lang": tweetData["data"]["lang"],
        "author": tweetAuthor,
        "quoteCount": tweetData["data"]["quote_count"],
        "replyCount": tweetData["data"]["reply_count"],
        "retweetCount": tweetData["data"]["retweet_count"],
        "analysis": analysis,
    }
    db.child("tweets").child(tweetID).set(tweetData)
    return jsonify(tweetID)

@app.route('/saveTweetInUserProfile', methods=["POST"])
def saveTweetInUserProfile():
    db.child("users/" + request.json["uid"] + "/savedTweets").push(
        request.json["tweetID"]
    )
    return "OK"

@app.route('/readTweetAnalysisFromDB', methods=["GET"])
def readTweetAnalysisFromDB():
    analysis = db.child("tweets/" + request.args["tweetID"] + "/analysis").get()
    return jsonify(analysis.val())

@app.route('/readAllTweetsFromDB', methods=["GET"])
def readAllTweetsFromDB():
    tweets = db.child("tweets/").get()
    return jsonify(tweets.val())

@app.route('/readUsersSavedTweets', methods=["GET"])
def readUsersSavedTweets():
    tweets = db.child("users/" +  request.args["uid"] + "/savedTweets").get()
    tweetInfo = []
    print(tweets.val())
    for elem in tweets.val().values():
        tweetInfo.append(db.child("tweets/" + elem).get().val())
    return jsonify(tweetInfo)

@app.route('/readUsersInfoFromDB', methods=["GET"])
def readUsersInfoFromDB():
    userInfo = db.child("users/" +  request.args["uid"]).get()
    return jsonify(userInfo.val())


if __name__ == '__main__':
    app.run(debug=True)
