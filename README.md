# TravelPerk Django Exercise

Details and API specification:
https://docs.google.com/presentation/d/1bgdFJ7jffokCkguBcQLQ69aEqquQLJPyLQurzdbDZVE/edit?usp=sharing

### To run unit tests

Run ```docker-compose run --rm app sh -c "python manage.py test"```

### To start local server

1. Create a Docker `.env` file in the project root containing the secret values for these environment properties:

````
POSTGRES_PASSWORD
DJANGO_SECRET_KEY
````

2. Run ```docker-compose up```

API endpoints will be available at http://0.0.0.0:8000, e.g.

`http://0.0.0.0:8000/recipes/`

`http://0.0.0.0:8000/recipes/{recipe_id}/`

### To stop local server

Run ```docker-compose down```
