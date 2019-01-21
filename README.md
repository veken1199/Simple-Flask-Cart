# Shopify Challenge - Backend Intern - Winter 2019
live version: https://challenge-2019.herokuapp.com/

## About the Application:
This web service is built using Python flask. For data persistence, I used SQLAlchemy toolkit that also provides Object
Relational Mapper. For persistence layer, SQLAlchemy is configured to use sqlite3 which is hosted locally on the disk.
Since we are dealing with APIs that could accept and return different types of data, I wanted to experiment with data
serialization tool which is called Marshmallow. I am using those two tools for the first time; however,
it is very interesting approach to interact with database and prepare API responses.

With the help of Marshmallow Schemas and Swagger I was able to auto generate API Docs and host them on `localhost:5000/swagger-u`
and `https://challenge-2019.herokuapp.com/swagger-ui` with little markups.

There were some limitations in this approach such as when I wanted to auto document an endpoint that accepts GET
'arguments', Apispec could not pick up the allowed args.
It also automatically creates API docs for OPTIONS http functions that are activated in flask by default.

Further more, the app has been containerized and deployed on a remote `https://challenge-2019.herokuapp.com/`

Or, you can run the application, and the documentation can be accessed from [localhost:5000/](http://localhost:5000/)

### Run the app:
- Preparing the env
```
// Using Virtual Environment
pip install virtualenv
// Linux
virtualenv venv
source bin/activate
```
```
// windows
python -m virtualenv venv
venv\Script\Activate
```
- Installing the dependencies
```
// Installing the required libs
pip install -r requirements.txt
// Setup the database
python setup.py
// Run the app
python main.py
// The app should start on http://localhost:5000
```
#### Using docker
```
docker build -t dockershopifyapp .
// Run the docker container
docker run -p 5000:5000 dockershopifyapp
// The app should start on http://localhost:5000
```
#### Using DockerToolbox (windows)
```
docker-compose up
// the app should start on http://192.168.99.100:5000
```

#### Run the tests:
```
// Use nosetests to run the tests: in virtualenv
nosetests

// In windows
python -m nose
```