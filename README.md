# Chatboard -project
The idea of the project is to create a chatboard web-application, where users can create threads and reply to them with posts.

## Current application functions

* Users can login and logout
* Users can register new accounts
* Users can create new threads
* Users can view other user's profiles
* Users can see all threads
* Users can edit and delete posts
* Users can see if posts have been edited
* Users can edit their profiles and add profile pics
* A post has the username and profile pic of the poster
* Users can search for threads or posts
* Users can become admins
* Admins can delete any threads, but no posts or edit posts
* User page shows user's posts
* User can select a topic when creating a new thread

## Setup and installation

First create a virtual environment
```
python3 -m venv venv && source venv/bin/activate
```
Install flask
```
pip install flask
```

In order to initialize the database, run

```
flask init-db && mkdir static/uploads
```

Then to start the application, run

```
flask run
```

## Large data testing


## Use of AI
The official LLM model of the university of Helsinki, CurreChat, has been used in optimizing code and helping with HTML/CSS code.


