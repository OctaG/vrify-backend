from flask import *
import pyrebase

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

if __name__ == '__main__':
    app.run(debug=True)
