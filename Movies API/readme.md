
# Movies API

## Routes

**Display Movies**
URL
```
/movies
```
- Methods
    - GET 
        Returns Detail for all the movies
    - POST
        Expected format
            ```json
            {
                "title": "The Shawshank Redemption",
                "runtime": 142.0,
                "genres": ["Crime", "Drama"],
                "rating": 9.3,
                "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                "director": "Frank Darabont",
                "year": 1994
            }
            ```

**Get Single Movie Data**
URL
```
/movies/<_id>
```

- Methods
    - GET

**Update Movie**
URL
```
/movies/<_id>/update
```

- Methods
    - PUT

**Delete Movie**
URL
```
/movies/<_id>/delete
```

- Methods
    - DELETE


**Get Movies By Genre**
URL
```
/movies/genre/<string:genre>
```

Returns all the movies with given `genre`

- Methods
    - GET

**Get Movies By Year**
URL
```
/movies/year/<int:year>
```

Returns all the movies with given `year`

- Methods
    - GET
