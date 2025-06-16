import sqlite3
import re
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
import forum, db
from errors import *



def validate_username(username):
    # Username must be 3-20 characters long and contain only letters, numbers, and underscores
    return re.match(r"^\w{3,20}$", username) is not None


def login_user(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"

    try:
        user_id, password_hash = db.query(sql, [username])[0]
        if check_password_hash(password_hash, password):
            user = forum.get_user_by_id(user_id)
            session["username"] = username
            session["user_id"] = user_id
            session["profile_picture"] = user["profile_picture"]
            session["is_admin"] = user["is_admin"]
        else: 
            raise PasswordsDoNotMatch
    except (IndexError, PasswordsDoNotMatch):
        return "Error: wrong username or password"


def create_user(username, password1, password2):
        
    if not validate_username(username):
        return "Error: Invalid username. Must be 3-20 characters long and contain only letters, numbers, and underscores."

    if password1 != password2:
        return "Error: Passwords do not match."

    password_hash = generate_password_hash(password1)

    try:
        forum.create_user(username, password_hash)
    except sqlite3.IntegrityError:
        return "Error: Username taken."