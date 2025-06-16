import sqlite3
import re
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
import forum, db
from errors import *



def validate_username(username):
    # Username must be 3-20 characters long and contain only letters, numbers, and underscores
    return re.match(r"^\w{3,20}$", username) is not None

def username_exists(username):
    sql = "SELECT 1 FROM users WHERE username = ?"
    return db.query(sql, [username]) != []


def login_user(username, password):
    validate_username(username)

    sql = "SELECT id, password_hash FROM users WHERE username = ?"

    user_id, password_hash = db.query(sql, [username])[0]
    if check_password_hash(password_hash, password):
        user = get_user_by_id(user_id)
        session["username"] = username
        session["user_id"] = user_id
        session["profile_picture"] = user["profile_picture"]
        session["is_admin"] = user["is_admin"]
    else: 
        raise PasswordsDoNotMatch

def register_user(username, password1, password2):
        
    if not validate_username(username):
        return "Error: Invalid username. Must be 3-20 characters long and contain only letters, numbers, and underscores."

    if password1 != password2:
        return "Error: Passwords do not match."

    password_hash = generate_password_hash(password1)

    if not username_exists(username):
        create_user(username, password_hash)
    else: raise UserAlreadyExists


def get_user_by_id(user_id):
    sql = "SELECT username, full_name, bio, university, profile_picture, is_admin FROM users WHERE id = ?"
    try:
        result = db.query(sql, [user_id])[0]
    except IndexError as e:
        return None
    return result

def get_user_with_username(username:str):

    another_profile = """SELECT username,
        full_name, bio,
        profile_picture, university, created_at
        FROM users
        WHERE username = ?
        """
    
    own_profile = """SELECT username,
        full_name, bio,
        profile_picture, university, is_admin, created_at
        FROM users
        WHERE username = ?
        """
    
    if username == session.get("username"):
        sql = own_profile
    else:
        sql = another_profile

    try:
        user = db.query(sql, [username])[0]
    except IndexError:
        return "Error: No such profile found"
    return user

def create_user(username, password_hash, profile_picture="static/images/mysterious_avatar.jpg"):
    sql = "INSERT INTO users (username, password_hash, profile_picture) VALUES (?, ?, ?)"
    db.execute(sql, [username, password_hash, profile_picture])

def update_user_profile(user_id, full_name, bio, university, profile_picture_url, is_admin):
    sql = """
        UPDATE users
        SET full_name = ?, 
            bio = ?, 
            university = ?, 
            profile_picture = ?,
            is_admin = ?
        WHERE id = ?;
        """
    db.execute(sql, [full_name, bio, university, profile_picture_url, is_admin, user_id])