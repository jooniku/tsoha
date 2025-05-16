from flask import Flask, session, request, url_for, redirect, render_template, current_app
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash
import config
import db

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

@app.route("/user_page")
def user_page():
    """Return user page if logged in. Else goto login.

    Returns:
        _type_: _description_
    """
    if "username" in session:
        return render_template("userpage.html")
    return render_template("loginpage.html")

@app.route("/all_threads", methods=["GET", "POST"])
def all_threads():
    return render_template("all_threads.html")

@app.route("/login", methods=["POST"])
def login():
    """Login function. Taken from the course material.

    Returns:
        _type_: Main page or error
    """
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql, [username])[0][0]
    print(password_hash)

    if check_password_hash(password_hash, password):
        session["username"] = username
        print(session["username"])
        return redirect("/")
    else: return "Error: wrong username or password"

@app.route("/logout")
def logout():
    session.clear()
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