from flask import flash, session
import db


def get_thread(thread_id):
    """Get thread by id.

    Args:
        thread_id (int)
    """
    sql = """SELECT threads.id, threads.title, threads.user_id, threads.created_at,
        threads.topic_id, topics.name AS topic_name,
        (SELECT COUNT(*) FROM posts WHERE posts.thread_id = threads.id) AS total,
        (SELECT MAX(created_at) FROM posts WHERE posts.thread_id = threads.id) AS last
        FROM threads
        LEFT JOIN topics ON threads.topic_id = topics.id
        WHERE threads.id = ?"""
    return db.query(sql, [thread_id])[0]

def get_thread_id_by_post(post_id):
    sql = "SELECT thread_id FROM posts WHERE id = ?"
    return db.query(sql, [post_id])[0][0]

def get_post_by_id_and_user(post_id, user_id):
    try:
        sql = """SELECT thread_id, content,
        created_at, reply_to, edited, edit_time, deleted
        FROM posts WHERE id = ? AND user_id = ?"""
        return db.query(sql, [post_id, user_id])[0]
    except IndexError as e:
        return None
    
def thread_count():
    sql = "SELECT COUNT(id) FROM threads"
    return db.query(sql)[0][0]

def post_count():
    sql = "SELECT COUNT(id) FROM posts"
    return db.query(sql)[0][0]

def get_posts(thread_id):
    """Get all posts to a specific thread.
    """
    sql = """SELECT p.id, p.content, p.created_at, p.user_id, p.reply_to,
            p.deleted, p.edited, p.edit_time, u.username, u.profile_picture
            FROM posts p, users u
            WHERE p.user_id = u.id AND p.thread_id = ?
            ORDER BY p.id"""
    return db.query(sql, [thread_id])

def get_posts_by_username(username):
    sql = """
        SELECT p.id, p.content, p.created_at, p.thread_id, users.profile_picture, threads.title AS thread_title
        FROM posts p
        JOIN users ON p.user_id = users.id
        JOIN threads ON p.thread_id = threads.id
        WHERE users.username = ?
        ORDER BY p.created_at DESC
    """
    return db.query(sql, [username])


def get_page_threads(page, page_size):
    sql = """
        SELECT threads.id, threads.title, threads.topic_id, topics.name AS topic_name,
               COUNT(posts.id) AS total, MAX(posts.created_at) AS last
        FROM threads
        LEFT JOIN topics ON threads.topic_id = topics.id
        LEFT JOIN posts ON posts.thread_id = threads.id
        GROUP BY threads.id
        ORDER BY last DESC NULLS LAST
        LIMIT ? OFFSET ?;
    """
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])


def get_all_topics():
    sql = "SELECT id, name FROM topics"
    return db.query(sql)

def add_topic(topic):
    sql = "INSERT INTO topics (name) VALUES (?)"
    db.execute(sql, [topic])

def add_thread(title, content, topic_id, user_id):
    """Add a new thread. Also adds the first post.

    Args:
        title (str): _description_
        content (str): _description_
        topic_id (int): _description_
        user_id (int): _description_

    Returns:
        int: _description_
    """
    sql = "INSERT INTO threads (title, topic_id, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, topic_id, user_id])
    thread_id = db.last_insert_id()
    add_post(content=content, user_id=user_id, thread_id=thread_id)
    flash("Thread created successfully")
    return thread_id
    
def add_post(content, user_id, thread_id, reply_to=None):
    """Add new post.
    """
    sql = """INSERT INTO posts (content, created_at, user_id, thread_id, reply_to)
             VALUES (?, datetime('now'), ?, ?, ?)"""
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

def delete_thread(thread_id):
    """Delete thread. Does not require
    user_id to be the same as thread
    Due to admin users being able to delete threads."""
    
    delete_all_posts_on_thread(thread_id=thread_id)
    
    sql = """DELETE FROM threads WHERE id = ?"""
    db.execute(sql, [thread_id])

def delete_all_posts_on_thread(thread_id):
    sql = "DELETE FROM posts WHERE thread_id = ?"
    db.execute(sql, [thread_id])

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

