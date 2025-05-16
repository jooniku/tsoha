from flask import Flask, flash,  session, request, redirect, render_template, current_app
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import config
import db
from errors import *

app = Flask(__name__, template_folder="templates")
app.secret_key = config.secret_key

# Register teardown
db.init_app(app)

@app.cli.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.init_db()
    print("Initialized the database")

@app.route("/")
def index():
    res = db.query("SELECT * FROM Users")
    print(res)
    for i in res[0]:
        print(i)
    return render_template("index.html")

@app.route("/loginpage")
def loginpage():
    return render_template("loginpage.html")

@app.route("/registerpage")
def registerpage():
    return render_template("/registerpage.html")

@app.route("/userpage")
def user_page():
    """Return user page if logged in. Else goto login.

    Returns:
        _type_: _description_
    """
    if "username" in session:
        return render_template("userpage.html")
    flash("Error: Log in to view user page")
    return render_template("loginpage.html")

@app.route("/all_threads", methods=["GET", "POST"])
def all_threads():
    return render_template("all_threads.html")

@app.route("/login", methods=["POST"])
def login():
    """Login function. Taken from the course material.
    Changed some parts.

    Returns:
        _type_: Main page or error
    """
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT password_hash FROM users WHERE username = ?"

    try:
        password_hash = db.query(sql, [username])[0][0]
        if check_password_hash(password_hash, password):
            session["username"] = username
            print(session["username"])
            return redirect("/")
        else: raise PasswordsDoNotMatch
    except (IndexError, PasswordsDoNotMatch):
        return "Error: wrong username or password"


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "Error: Passwords do not match."
    
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "Error: username taken."

    flash("Your registration was successful!")
    return redirect("/loginpage")
    

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect("/")



'''l = db.execute("""
            INSERT INTO users (username, email, password_hash, full_name, bio, profile_picture, university, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
            'dummy_user',
            'dummy@example.com',
            'hashedpassword123',
            'Dummy User',
            'Just a test user.',
            '/static/images/dummy.png',
            'Test University',
            0  # not admin
            ))
'''