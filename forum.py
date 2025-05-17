import flask
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
             FROM posts, users u
             WHERE p.user_id = u.id AND p.thread_id = ?
             ORDER BY p.id"""
    return db.query(sql, [thread_id])


