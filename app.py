from flask import Flask
from flask import render_template, current_app
from flask.cli import with_appcontext
import db

app = Flask(__name__, template_folder="templates")
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

@app.route("/user_page")
def user_page():
    return render_template("userpage.html")

@app.route("/message_board")
def message_board():
    return render_template("message_board.html")



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