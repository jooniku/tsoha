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
cd tsoha && flask init-db && mkdir static/uploads && python3 seed.py
```

Then to start the application, run

```
flask run
```

## Testing with large amounts of data
### Basic test
Testing with large amounts of data was done as instructed in the materials after all optimizations. The code is in the "seed.py" file.

Login/registration were not affected and both took 0.0 seconds.

Rendering new pages was not affected and took 0.0 seconds.

Search was also not affected by 10 000 threads and the search for "thread" took 0.0 seconds.

### Large test
In this test the amount of the data were increased by __100X__. There were close to 10 000 000 posts and 1 000 000 threads.

The loading of the home page took 25.9 seconds.

The loading of the all_threads page took 36.9 seconds.

Logging in took 23.55 seconds.

Registration was not affected and took 0.0 seconds.

Creating a new thread took 1.29 seconds.



## Use of AI
The official LLM model of the university of Helsinki, CurreChat, has been used in optimizing code and helping with HTML/CSS code.


