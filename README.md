# Chatboard -project
The idea of the project is to create a chatboard web-application, where users can create threads and reply to them. 

## Current application functions

* Users can login and logout
* Users can register new accounts
* Users can create new threads
* Users can view other user's profiles
* Users can see all threads
* Users can edit and delete posts
* Users can edit their profiles and add profile pics
* A post has the username and profile pic of the poster
* Users can search for threads or posts

## Future application functions

* Users can delete their profiles
* Admin users can delete posts/threads, but not edit
* Posts can include images

## Setup and installation

First create a virtual environment
```
python3 -m venv venv
```
Install flask
```
pip install flask
```

In order to initialize the database, run

```
flask init-db
```

Then to start the application, run

```
flask run
```


