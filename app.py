from flask import Flask, flash,  session, request, redirect, render_template, abort
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import config
import db
from errors import *
import forum

app = Flask(__name__, template_folder="templates")
app.secret_key = config.SECRET_KEY

# Register teardown
db.init_app(app)

def authenticate_user(username:str=None):
    """Helper function to check
    that user is logged in. 

    If username is given, the function makes sure
    it corresponds to session user. For example, when
    changing a users information the session user and the profile
    must be equal.

    If no user is provided, the function makes sure
    there is a user logged in. For example when posting to a thread.
    """
    if username:
        if username != session["username"]:
            abort(403)
    else: # needs to be just logged in
        if "username" not in session: # just logged in
            abort(403)

def allowed_file(filename):
    """Check if file is in the allowed extensions.
    Configured in the config file

    Args:
        filename (str): filename

    Returns:
        bool
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.cli.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.init_db()
    print("Initialized the database")

@app.route("/")
def index():
    return render_template("/index.html")

@app.route("/login_page")
def login_page():
    return render_template("/login_page.html")

@app.route("/register_page")
def register_page():
    return render_template("/register_page.html")

@app.route("/user/<username>")
def user_page(username:str):
    """Return user page if logged in. Else goto login.

    Returns:
        _type_: _description_
    """

    another_profile = """SELECT username,
        full_name, bio,
        profile_picture, university
        FROM users
        WHERE username = ?
        """
    
    own_profile = """SELECT username,
        email, full_name, bio,
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

    return render_template("/user_page.html", user=user)

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    authenticate_user("lll")
    # not finished
    
@app.route("/all_threads", methods=["GET", "POST"])
def all_threads():
    return render_template("/all_threads.html", threads=forum.get_all_threads())


@app.route("/thread/<int:thread_id>")
def show_thread(thread_id):
    thread = forum.get_thread(thread_id)
    posts = forum.get_posts(thread_id)
    print(posts)
    return render_template("thread.html", thread=thread, posts=posts)

@app.route("/new_thread", methods=["POST"])
def new_thread():
    print(session)
    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]

    thread_id = forum.add_thread(title, content, user_id)
    return redirect("/thread/" + str(thread_id))


@app.route("/login", methods=["POST"])
def login():
    """Login function. Taken from the course material.
    Changed some parts.

    Returns:
        _type_: Main page or error
    """
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT id, password_hash FROM users WHERE username = ?"

    try:
        user_id, password_hash = db.query(sql, [username])[0]
        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
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
    return redirect("/login_page")
    

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect("/")


