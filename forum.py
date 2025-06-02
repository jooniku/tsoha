from flask import Flask, flash, session
import db


def get_thread(thread_id):
    """Get thread by id.

    Args:
        thread_id (int)
    """
    sql = "SELECT id, title, topic FROM threads WHERE id = ?"
    return db.query(sql, [thread_id])[0]

def get_thread_id_by_post(post_id):
    sql = "SELECT thread_id FROM posts WHERE id = ?"
    return db.query(sql, [post_id])[0][0]

def get_post_by_id_and_user(post_id, user_id):
    sql = "SELECT * FROM posts WHERE id = ? AND user_id = ?"
    return db.query(sql, [post_id, user_id])

def get_user_with_username(username:str):

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
    return user

def get_posts(thread_id):
    """Get all posts to a specific thread.
    """
    sql = """SELECT p.id, p.content, p.created_at, p.user_id, p.reply_to,
            p.deleted, p.edited, p.edit_time, u.username
            FROM posts p, users u
            WHERE p.user_id = u.id AND p.thread_id = ?
            ORDER BY p.id"""
    return db.query(sql, [thread_id])

def get_posts_by_username(username):
    sql = """
        SELECT posts.id, posts.content, posts.created_at, posts.thread_id, threads.title AS thread_title
        FROM posts
        JOIN users ON posts.user_id = users.id
        JOIN threads ON posts.thread_id = threads.id
        WHERE users.username = ?
        ORDER BY posts.created_at DESC
    """
    return db.query(sql, [username])


def get_all_threads():
    sql = """SELECT t.id, t.title, t.topic, COUNT(p.id) total, MAX(p.created_at) last
             FROM threads t, posts p
             WHERE t.id = p.thread_id
             GROUP BY t.id
             ORDER BY t.id DESC"""
    return db.query(sql)

def get_all_topics():
    sql = "SELECT id, name FROM topics"
    return db.query(sql)

def add_thread(title, content, topic, user_id):
    """Add a new thread. Also adds the first post.

    Args:
        title (str): _description_
        content (str): _description_
        topic (str): _description_
        user_id (int): _description_

    Returns:
        int: _description_
    """
    sql = "INSERT INTO threads (title, topic, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, topic, user_id])
    thread_id = db.last_insert_id()
    add_post(content, user_id, thread_id)
    flash("Thread created successfully")
    return thread_id
    
def add_post(content, user_id, thread_id, reply_to=None):
    """Add new post.
    """
    sql = """INSERT INTO posts (content, created_at, user_id, thread_id, reply_to)
             VALUES (?, datetime('now'), ?, ?, ?, ?)"""
    db.execute(sql, [content, user_id, thread_id, reply_to])
    flash("Post added successfully")

def edit_post(post_id, user_id, new_content):
    sql = """
        UPDATE posts
        SET content = ?, edited = 1, edit_time = CURRENT_TIMESTAMP
        WHERE id = ? AND user_id = ? AND deleted = 0
    """
    db.execute(sql, [new_content, post_id, user_id])


def delete_post(post_id, user_id):
    sql = """
        UPDATE posts
        SET deleted = 1, content = "[deleted]"
        WHERE id = ? AND user_id = ?
    """
    db.execute(sql, [post_id, user_id])


def find_post(query):
    """Function to search the formun's threads
    or posts using a keyword.
    """
    sql = """
        SELECT threads.id AS thread_id,
            threads.title AS thread_title,
            NULL AS post_id,
            NULL AS post_content
        FROM threads
        WHERE threads.title LIKE ?

        UNION

        SELECT threads.id AS thread_id,
            threads.title AS thread_title,
            posts.id AS post_id,
            posts.content AS post_content
        FROM threads
        JOIN posts ON threads.id = posts.thread_id
        WHERE posts.content LIKE ?
    """
    like = "%" + query + "%"
    return db.query(sql, [like, like])

