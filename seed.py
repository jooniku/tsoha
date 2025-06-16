import random
import sqlite3

db = sqlite3.connect("database.db")

# Clear existing data
db.execute("DELETE FROM posts")
db.execute("DELETE FROM threads")
db.execute("DELETE FROM users")
db.execute("DELETE FROM topics")

# Parameters
user_count = 1000
topic_count = 10
thread_count = 10**4  # reduce if too slow
post_count = 10**5    # reduce if too slow

# Add topics
for i in range(1, topic_count + 1):
    db.execute("INSERT INTO topics (name) VALUES (?)", [f"Topic {i}"])

# Add users
for i in range(1, user_count + 1):
    db.execute("""INSERT INTO users (username, password_hash, profile_picture)
                  VALUES (?, 'hashed_password', 'static/images/mysterious_avatar.jpg')""",
               [f"user{i}"])

# Add threads
for i in range(1, thread_count + 1):
    user_id = random.randint(1, user_count)
    topic_id = random.randint(1, topic_count)
    db.execute("""INSERT INTO threads (title, user_id, topic_id)
                  VALUES (?, ?, ?)""",
               [f"Thread {i}", user_id, topic_id])

# Add posts
for i in range(1, post_count + 1):
    user_id = random.randint(1, user_count)
    thread_id = random.randint(1, thread_count)
    db.execute("""INSERT INTO posts (thread_id, user_id, content, created_at)
                  VALUES (?, ?, ?, datetime('now'))""",
               [thread_id, user_id, f"Post content {i}"])

# Commit and close
db.commit()
db.close()
