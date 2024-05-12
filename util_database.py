import sqlite3
import os

ROOT = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(ROOT, "blog_content.db")
def initialize_database(path):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    query = '''CREATE VIRTUAL TABLE IF NOT EXISTS articles USING fts5 (
        article_id, article_title, creation_date, creation_time, total_views, article_content)'''
    cursor.execute(query)
    query = '''CREATE TABLE IF NOT EXISTS comments (
        comment_id TEXT,
        author TEXT,
        creation_date TEXT,
        creation_time TEXT,
        article_id TEXT,
        comment_content TEXT)'''
    cursor.execute(query)
    query = '''CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        email TEXT,
        password TEXT)'''
    cursor.execute(query)
    db.commit()
    db.close()
    print("Database succesfully initialized !")