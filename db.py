import sqlite3
from flask import g, current_app
from config import DATABASE, SCHEMA


def _get_db():
    """Provide connection to database

    Database is defined in config file

    Is called when connection to webpage is initialized

    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON")
    db.row_factory = sqlite3.Row
    return db


def _close_db(exception):
    """Close database connection

    Args:
        exception: given if context dies of an error
    """
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize database with schema from config file
    """
    db = _get_db()
    with current_app.open_resource(SCHEMA, mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()


def init_app(app):
    """Register current app to database connection

    Using this the connection will close properly

    Args:
        app: current app context
    """
    app.teardown_appcontext(_close_db)

def execute(sql, params=[]):
    db = _get_db()
    result = db.execute(sql, params)
    db.commit()
    g.last_insert_id = result.lastrowid


def query(sql, params=[]):
    db = _get_db()
    return db.execute(sql, params).fetchall()