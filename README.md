# Kpler-technical-challenge

# How to get started with the project

There are 2 main folder: `client` & `server`

## Server

I used the [Flask](https://flask.palletsprojects.com/en/3.0.x/) Framework to create a small backend server that stores vessels positions inside a sqlite database. The database is a single table consisting of vessels positions.


### Prerequisites

Have python3 and pip3 installed on your machine

### How to start the server


`cd server`

 - Create a virtual python environment

```virtualenv -p python3 .venv```

```. .venv/bin/activate```

 - Install dependencies

```pip3 install -r requirements.txt```

 - Initialise the Database

```python3 -m flask --app flaskr init-db```

 - Start the server

```python3 -m flask --app flaskr run --debug```




## Client

The client side is done with Vue3, I used Tailwind for styling,

Note: I used a different interface for `Vessel positions` between the server & client to highlight that in a real application, we don't need to have the exact same structure. What matters is that the FE/BE agree on the interface but each application is free to manage its data model the way it suits best.

### Prerequisites

Node 18

### How to start the client


`cd client`

 - Install dependencies

```npm i```

 - start the server

```npm start```

 - Open your browser on `http://localhost:5173/`


## Limitations of this app / Things to improve

### Server
The server is the most basic you can have for the requirements, I had to learn Python / Flask for this project, so I'm sure there are many things that can be greatly improved.

For instance, the validation on the server side is quite basic and should be improved. I did the validation of the position (valid latitude / longitude) on the client side for convenience because I have more experience in Front end but it should be done in the back end (maybe in both for basic validation)

There is no security in place in case anyone tries to attack the server

Error Management should be better: I raise error using `abort` directly, I should use a centralise Error handling

Logs: I put DEBUG logs everywhere but in a real application, we would differentiate "normal" logs from "Debug" logs

Docker: for a production server, I would create a docker container to run the server.

#### Unit test
I did not do any unit test for lack of time but there should be some

### Client

#### Importing Data using CSV
I did the most basic validation possible but there are many more validations we should do, for instance:

  - Validate that every coordinates in within a sea or ocean
  - Calculate the distance between 2 consecutive points for a given vessel and the time difference => reject if the speed of the vessel does not make sense 

These will apply to both the CSV import and the add Single position

#### Play Button
This is just a proof of concept, it will not work with huge amount of data and some performance optimisation would be needed to really use it. And aas it stands, it doesn't offer enough information to the user like which time it actually filters

#### Unit test
I did not do any unit test for lack of time but there should be some

#### Storybook
It will be nice to have storybook to give our designers an overview of all our components

#### CI/CD
A real app will have CI/CD where we would run linting, unit test, deploy on test / production automatically
