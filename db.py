import sqlite3

def create_db():
    conn = sqlite3.connect('all.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bug (userid INT, question TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS help (userid INT, question TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS admins (adminus TEXT)''')
    conn.commit()
    conn.close()



def add_bug(userid, question):
    conn = sqlite3.connect('all.db')
    c = conn.cursor()
    c.execute("INSERT INTO bug (userid, question) VALUES (?, ?)", (userid, question))
    conn.commit()
    conn.close()

def add_help(userid, question):
    conn = sqlite3.connect('all.db')
    c = conn.cursor()
    c.execute("INSERT INTO help (userid, question) VALUES (?, ?)", (userid, question))
    conn.commit()
    conn.close()

def get_bugs():
    conn = sqlite3.connect('all.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bug")
    bugs = c.fetchall()
    conn.close()
    return bugs

def get_helps():
    conn = sqlite3.connect('all.db')
    c = conn.cursor()
    c.execute("SELECT * FROM help")
    helps = c.fetchall()
    conn.close()
    return helps

def get_admins():
    conn = sqlite3.connect('all.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admins")
    admins = c.fetchall()
    conn.close()
    return admins

def add_admin(adminus):
    conn = sqlite3.connect('all.db')
    c = conn.cursor()
    c.execute("INSERT INTO admins (adminus) VALUES (?)", (adminus,))
    conn.commit()
    conn.close()

create_db()