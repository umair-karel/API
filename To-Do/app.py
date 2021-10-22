from flask import Flask, request, jsonify, url_for, session
from flask_pymongo import PyMongo
from bson.json_util import dumps
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

todos_collection = mongoClient.db.todos

######## Utils ########

# Generating unique 5 digit id for Documents
def generate_uuid(length=5):
    return uuid.uuid4().hex[:length]


######## Routes ########

# GET /todos -> Returns the detail for all the todos with status code 200 (success)
@app.route('/todos')
def home():
    todos = todos_collection.find()
    todos = [todo for todo in todos]

    return dumps(todos)

# POST /add -> Adds new todo and returns the same todo with status code 201 (created)
@app.route('/add', methods=['POST'])
def add():
    data = request.json
    print(data)
    data['_id'] = generate_uuid()
    todos_collection.insert_one(data)

    return dumps(data)

# PUT /update/<_id> -> Update/Add fields for todo item of given _id (status code 204 success)
@app.route('/update/<_id>', methods=['PUT'])
def update(_id):
    data = request.json
    todo = todos_collection.update_one({"_id": _id}, {'$set':data})
    
    return dumps(data)

# DELETE /delete/<_id> -> Deletes todo item of given _id from the database (status code 204 success)
@app.route('/delete/<_id>', methods=['DELETE'])
def delete(_id):
    todos_collection.delete_one({"_id": _id})
    
    return jsonify({'status': 'Deleted!'})




if __name__ == '__main__':
    app.run(debug=True)
