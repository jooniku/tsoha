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
    return render_template("index.html")

@app.route("/user_page")
def user_page():
    return render_template("userpage.html")

@app.route("/message_board")
def message_board():
    return render_template("message_board.html")