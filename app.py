from flask import Flask, flash,  session, request, redirect, render_template, abort, url_for
from flask.cli import with_appcontext
import user
import os, re
import config
import db
from errors import *
import forum

app = Flask(__name__, template_folder="templates")
app.secret_key = config.SECRET_KEY
app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER

# Register teardown
db.init_app(app)

def init_topics():
    topics = ["world domination", "moonlanding", "general", "general conspiracy", "lizard people"]
    for topic in topics:
        forum.add_topic(topic)

@app.context_processor
def inject_user():
    user = None
    if "user_id" in session:
        user = forum.get_user_by_id(session["user_id"])
    return dict(current_user=user)

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
    return "." in filename and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS


def secure_filename(filename):
    """
    Return a secure version of the provided filename.
    This function removes any potentially unsafe characters and ensures
    the filename is suitable for use in a filesystem.
    """
    filename = os.path.basename(filename)
    filename = filename.replace(" ", "_")    
    filename = re.sub(r"[^a-zA-Z0-9_.-]", "", filename)
    return filename

def compute_indent_levels(posts):
    posts_dict = {post["id"]: post for post in posts}
    indent_levels = {}

    def get_level(post_id):
        level = 0
        current = posts_dict.get(post_id)
        while current and current["reply_to"]:
            level += 1
            parent_id = current["reply_to"]
            current = posts_dict[parent_id] if parent_id in posts_dict else None
        return level

    for post in posts:
        indent_levels[post["id"]] = get_level(post["id"])

    return indent_levels, posts_dict

def get_latest_posts(num_posts=10):
    sql = """
        SELECT 
            posts.id AS post_id,
            posts.content,
            posts.created_at,
            posts.thread_id,
            threads.title AS thread_title,
            users.username
        FROM posts
        JOIN threads ON posts.thread_id = threads.id
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.created_at DESC
        LIMIT ?
        """
    return db.query(sql, [num_posts])


@app.cli.command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.init_db()
    init_topics()
    print("Initialized the database")


@app.route("/")
def index():
    posts=get_latest_posts()
    return render_template("/index.html", posts=posts)

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
    user = forum.get_user_with_username(username)
    posts = forum.get_posts_by_username(username)

    return render_template("/user_page.html", user=user, posts=posts)

    
@app.route("/all_threads", methods=["GET", "POST"])
def all_threads():
    topics = db.query("SELECT id, name FROM topics")
    threads = forum.get_all_threads()
    topics = forum.get_all_topics()


    return render_template("/all_threads.html", threads=threads, topics=topics)


@app.route("/thread/<int:thread_id>")
def show_thread(thread_id):
    thread = forum.get_thread(thread_id)
    posts = forum.get_posts(thread_id)
    topics = forum.get_all_topics()
    
    indent_levels, posts_dict = compute_indent_levels(posts)
    return render_template("thread.html", thread=thread, posts=posts, indent_levels=indent_levels, posts_dict=posts_dict, topics=topics)


@app.route("/new_thread", methods=["POST"])
def new_thread():
    authenticate_user()
    title = request.form["title"]
    content = request.form["content"]
    topic_id = request.form["topic_id"]
    user_id = session["user_id"]
    print(session.get("profile_picture"))

    thread_id = forum.add_thread(title=title, content=content, topic_id=topic_id, user_id=user_id)
    return redirect("/thread/" + str(thread_id))

@app.route("/reply/<int:post_id>", methods=["POST"])
def reply(post_id):
    authenticate_user()
    content = request.form.get("content", "").strip()
    user_id = session.get("user_id")

    if not content:
        flash("Reply content cannot be empty.", "error")
        thread_id = forum.get_thread_id_by_post(post_id)
        return redirect(url_for("show_thread", thread_id=thread_id, reply_to=post_id))

    thread_id = forum.get_thread_id_by_post(post_id)
    if thread_id is None:
        flash("Invalid post or thread.", "error")
        return redirect(url_for("index"))
    
    forum.add_post(content=content, user_id=user_id, thread_id=thread_id, reply_to=post_id)

    flash("Reply posted successfully!", "success")
    return redirect(url_for("show_thread", thread_id=thread_id))

@app.route("/remove/<int:post_id>", methods=["POST"])
def remove(post_id):
    authenticate_user()

    user_id = session["user_id"]

    forum.delete_post(post_id, user_id)

    thread_id = forum.get_thread_id_by_post(post_id)
    if thread_id:
        return redirect(f"/thread/{thread_id}")

    return redirect("/")

@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit(post_id):
    authenticate_user()

    user_id = session["user_id"]
    
    post = forum.get_post_by_id_and_user(post_id, user_id)
    if not post:
        return "Post not found or you don't have permission", 404

    if request.method == "POST":
        content = request.form.get("content")
        if not content or content.strip() == "":
            error = "Content cannot be empty."
            return render_template("edit_post.html", post=post, error=error)

        forum.edit_post(post_id, user_id, content.strip())
        return redirect(f"/thread/{post['thread_id']}")

    return render_template("edit_post.html", post=post)


@app.route("/login", methods=["POST"])
def login():
    """Login function. Taken from the course material.
    Changed some parts.

    Returns:
        _type_: Main page or error
    """
    username = request.form["username"]
    password = request.form["password"]
    
    user.login_user(username, password)
    
    flash("Login successful!")
    return redirect("/")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    user.create_user(username, password1, password2)

    flash("Your registration was successful!")
    return redirect("/login_page")

    

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect("/")

        
@app.route("/find_post")
def find_post():
    query = request.args.get("query")
    if query:
        results = forum.find_post(query)
    else:
        query = ""
        results = []
    return render_template("find_post.html", query=query, results=results)

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    authenticate_user()

    user_id = session["user_id"]
    user = forum.get_user_by_id(user_id)

    if request.method == "POST":
        full_name = request.form["full_name"]
        bio = request.form["bio"]
        university = request.form["university"]
        is_admin = "is_admin" in request.form

        profile_picture_file = request.files["profile_picture_file"]
        if profile_picture_file and profile_picture_file.filename != "":
            filename = secure_filename(profile_picture_file.filename)
            if allowed_file(filename):
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                profile_picture_file.save(filepath)
                profile_picture_url = filepath
            else:
                flash(f"Invalid file type. Allowed types are: {config.ALLOWED_EXTENSIONS}")
                return redirect(url_for("edit_profile"))
        else:
            profile_picture_url = user["profile_picture"]

        forum.update_user_profile(user_id, full_name, bio, university, profile_picture_url, is_admin)
        session["is_admin"] = is_admin

        flash("Profile updated successfully.")
        return redirect(url_for("edit_profile"))

    return render_template("edit_profile.html", user=user)

@app.route("/thread/delete/<int:thread_id>", methods=["POST"])
def delete_thread(thread_id):
    thread = forum.get_thread(thread_id)
    if session.get("user_id") != thread["user_id"] and not session.get("is_admin", False):
        abort(403)

    forum.delete_thread(thread_id)

    flash("Thread deleted successfully.")
    return redirect(url_for("all_threads"))