from flask import Flask, flash
import db


def get_thread(thread_id):
    """Get thread by id.

    Args:
        thread_id (int)
    """
    sql = "SELECT id, title FROM threads WHERE id = ?"
    return db.query(sql, [thread_id])[0]

def get_posts(thread_id):
    """Get all posts to a specific thread.
    """
    sql = """SELECT p.id, p.content, p.created_at, p.user_id, u.username
             FROM posts p, users u
             WHERE p.user_id = u.id AND p.thread_id = ?
             ORDER BY p.id"""
    return db.query(sql, [thread_id])

def get_all_threads():
    sql = """SELECT t.id, t.title, COUNT(p.id) total, MAX(p.created_at) last
             FROM threads t, posts p
             WHERE t.id = p.thread_id
             GROUP BY t.id
             ORDER BY t.id DESC"""
    return db.query(sql)

def add_thread(title, content, user_id):
    """Add a new thread. Also adds the first post.

    Args:
        title (str): _description_
        content (str): _description_
        user_id (int): _description_

    Returns:
        int: _description_
    """
    sql = "INSERT INTO threads (title, user_id) VALUES (?, ?)"
    db.execute(sql, [title, user_id])
    thread_id = db.last_insert_id()
    add_post(content, user_id, thread_id)
    flash("Thread created successfully")
    return thread_id
    
def add_post(content, user_id, thread_id):
    """Add new post.
    """
    sql = """INSERT INTO posts (content, created_at, user_id, thread_id)
             VALUES (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, thread_id])
    flash("Post added successfully")
