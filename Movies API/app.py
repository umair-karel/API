from flask import Flask, request, jsonify, url_for, session
from flask_pymongo import PyMongo
from bson.json_util import dumps
from dotenv import load_dotenv
import uuid
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
mongoClient = PyMongo(app)

movies_collection = mongoClient.db.movies

######## Utils ########

# Generating unique 5 digit id for Documents
def generate_uuid(length=5):
    return uuid.uuid4().hex[:length]


######## Routes ########

# GET /movies -> Returns the detail for all the movies with status code 200 (success)
# POST /movies -> Adds new movie and returns the same movie with status code 201 (created)
@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        data = request.json
        data['_id'] = generate_uuid()

        movies_collection.insert_one(data)
        return jsonify({'messsage': 'Movie added to the db!'})

    else:
        movies = movies_collection.find()
        movies = [movie for movie in movies]

        return dumps(movies)


# PUT /movies/<_id> -> Returns the detail for a movie of given _id (status code 204 success)
@app.route('/movies/<_id>', methods=['GET'])
def movie(_id):
    movie = movies_collection.find_one({"_id": _id})
    
    return dumps(movie)


# PUT /update/<_id> -> Update/Add fields for movie item of given _id (status code 204 success)
@app.route('/movies/<_id>/update', methods=['PUT'])
def update(_id):
    data = request.json
    movie = movies_collection.update_one({"_id": _id}, {'$set':data})
    movie = movies_collection.find_one({"_id": _id})
    
    return dumps(movie)


@app.route('/movies/genre/<string:genre>', methods=['GET'])
def get_movies_by_genre(genre):
    movies = movies_collection.find({ 'genres': genre })
    print(movies)
    movies = [movie for movie in movies]

    return dumps(movies)


@app.route('/movies/year/<int:year>', methods=['GET'])
def get_movies_by_year(year):
    movies = movies_collection.find({ 'year': year })
    movies = [movie for movie in movies]

    return dumps(movies)


# DELETE /delete/<_id> -> Deletes movie item of given _id from the database (status code 204 success)
@app.route('/movies/<_id>/delete', methods=['DELETE'])
def delete(_id):
    movies_collection.delete_one({"_id": _id})
    
    return jsonify({'status': 'Deleted!'})



if __name__ == '__main__':
    app.run(debug=True)


# POST FORMAT
# {
#     "title": "The Shawshank Redemption",
#     "runtime": 142.0,
#     "genres": [],
#     "rating": 9.3,
#     "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
#     "director": "Frank Darabont",
#     "year": 1994
# }