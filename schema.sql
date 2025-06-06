-- Users table: student accounts with profile info and admin flag
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    bio TEXT,
    profile_picture TEXT NOT NULL,  -- URL or file path
    university TEXT,
    is_admin BOOLEAN DEFAULT 0,  -- 1 = admin, 0 = regular user
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Threads: discussion starters
CREATE TABLE threads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(topic_id) REFERENCES topics(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Posts: replies in threads
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reply_to INTEGER REFERENCES posts(id),
    edited BOOLEAN DEFAULT 0,
    edit_time DATETIME DEFAULT None,
    deleted BOOLEAN DEFAULT 0,
    FOREIGN KEY(thread_id) REFERENCES threads(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);


-- Images table: can be linked to either threads or posts
CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id INTEGER,
    post_id INTEGER,
    image_url TEXT NOT NULL,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(thread_id) REFERENCES threads(id),
    FOREIGN KEY(post_id) REFERENCES posts(id),
    CHECK (thread_id IS NOT NULL OR post_id IS NOT NULL)  -- must be linked to at least one
);

-- Topics table
CREATE TABLE topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
