import sqlite3

def create_db():
    conn = sqlite3.connect('all.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bug (userid INT, question TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS help (userid INT, question TEXT)''')
    conn.commit()
    conn.close()

def add_bug(userid, question):