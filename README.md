# foodgram
![example workflow](https://github.com/Alfaram/foodgram-project-react/actions/workflows/main.yml/badge.svg)  

# Website Foodgram: Grocery assistant
### Service description:

In this service, users can log in, publish recipes, subscribe to publications of other users, create a list of favorites, create a shopping list and download this list. After registration, users receive an authorization token. To add recipes, users must select ingredients from the database and tags (for example, breakfast), quantity, add an image, text and cooking time, all fields are required.

Additionally configured CI/CD(Continuous Integration and Continuous Deployment) for this project:
  - automatic start of tests(pep8),
  - building or updating the docker image in the container on Docker Hub; 
  - automatic deployment to the production server;


### **Stack**
![python version](https://img.shields.io/badge/Python-3.7-green)
![django version](https://img.shields.io/badge/Django-2.2-green)
![sorl-thumbnail version](https://img.shields.io/badge/Django%20REST%20Framework-%203.12.4-green)
![python version](https://img.shields.io/badge/Nginx-%201.18-green)
![python version](https://img.shields.io/badge/Docker-3.8-green)

### Run project in Docker

Clone project from:
```
git clone git@github.com:Alfaram/foodgram-project-react.git
```
Install and activate virtual environment. Then go to:
```
cd /infra
```
Start up projet by running :
```
docker-compose up
```
Need to create file .env in directory /foodgram/foodgram
Sample of env-file located in /foodgram/foodgram .env.example

Run next commands in rotation:

```
docker compose exec backend python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --no-input
```

### .env content template (not included in current repository) located at infra/.env path
```

SECRET_KEY=<django project secret key>
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<postgres database name>
DB_USER=<DB user>
DB_PASSWORD=<password>
DB_HOST=<db>
DB_PORT=<5432>
                    
```
