# Maintenance Tracker PostgreSQL API #

A set of API end points

* POST /api/v2/auth/signup - Register a user 
* POST /api/v2/auth/login - Login a user 
* GET /api/v2/users/requests - Fetch all requests for a logged in user
* GET /api/v2/users/requests/<prob_id> - Fetch a particular request for a logged in user
* PUT /api/v2/users/requests/<requestId> - Modifies a request for a logged in user only if not approved



## Pre-requisites ##

* Python
* Flask
* PostgreSQL

### Getting Started ###

* Clone repository
* Install `pip install -r requirements.txt`

### Running tests ###

`nosetests`
`postman` -To test the API end points

### Author ###

Elijah Ayeeta
