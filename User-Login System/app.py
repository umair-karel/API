from flask import Flask, request, jsonify, url_for, session
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import uuid
import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongoClient = PyMongo(app)
bcrypt = Bcrypt(app)
db = mongoClient.db

# Generating unique 5 digit id for Documents
def generate_uuid(length=5):
    return uuid.uuid4().hex[:length]

def valid_details(data):
    if 'name' in data and 'email' in data and 'password' in data:
        return True
        
    return False

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    if data:
        # Check if all the details are provided
        if valid_details(data):
            hashed_pwd = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            # Create the user object
            user = {
              "_id": generate_uuid(6),
              "name": data['name'],
              "email": data['email'],
              "password": hashed_pwd
            }

            # Check for existing email address
            if db.users.find_one({ "email": user['email'] }):
                return jsonify({ "error": "Email address already in use" }), 400

            db.users.insert_one(user)

            return jsonify({ "message": "signup successful!" }), 201
        else:
            return jsonify({ "error": "Some fields are missing" }), 400
    else:
        return jsonify({ "error": "Signup failed" }), 400


@app.route('/login', methods=['POST'])
def login():
    user = db.users.find_one({
      "email": request.json['email']
    })

    if user and bcrypt.check_password_hash(user['password'], request.json['password']):
        return jsonify({ "message": f"{user['name']} logged in successfully!!" }), 200    

    return jsonify({ "error": "Invalid login credentials" }), 401


if __name__ == "__main__":
    app.run(debug=True)
