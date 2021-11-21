import requests
import json
import re

rapidapi_key = ""

def getTweetID(url):
    return url.split('/')[-1]

def getTweetAuthor(url):
    return url.split('/')[-3]

def getTweetData(tweetID):
    url = "https://twitter32.p.rapidapi.com/getTweetById"
    querystring = {"tweet_id": tweetID}
    headers = {
        'x-rapidapi-host': "twitter32.p.rapidapi.com",
        'x-rapidapi-key': rapidapi_key
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)

def cleanText(tweetText):
    return ' '.join(re.sub(
        "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", tweetText).split()
        )

def analyzeTweet(tweetText):
    url = "https://fake-news-detection1.p.rapidapi.com/"
    querystring = {"text":tweetText}
    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "fake-news-detection1.p.rapidapi.com",
        'x-rapidapi-key': rapidapi_key
    }
    response = requests.request(
        "POST",
        url,
        data={},
        headers=headers,
        params=querystring,
    )
    return json.loads(response.text)["prediction"]
