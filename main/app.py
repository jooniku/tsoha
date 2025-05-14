from flask import Flask
from flask import render_template

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user_page")
def user_page():
    return render_template("userpage.html")

@app.route("/message_board")
def message_board():
    return render_template("message_board.html")