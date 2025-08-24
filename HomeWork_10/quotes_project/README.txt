1. docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres

2. cd ./quotes_project
3. python manage.py makemigrations authors
4. python manage.py makemigrations quotes
5. python manage.py migrate
6. python migrate_mongo_to_postgres.py

7. python manage.py createsuperuser
8. python manage.py runserver

# .env 
MONGO_URI = "mongodb+srv://mitus66:IqE0HmNGp5H2MOy9@cluster0.qzzbjox.mongodb.net/mongodb_1?retryWrites=true&w=majority&appName=Cluster0"

POSTGRES_DB = postgres
POSTGRES_USER = postgres
POSTGRES_PASSWORD = postgres
POSTGRES_HOST = localhost
POSTGRES_PORT = 5432
