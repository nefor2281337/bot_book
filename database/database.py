import sqlite3 as sq

def set_page_one(user_id):
    with sq.connect('users.db') as con:
        cursor = con.cursor()

        cursor.execute('UPDATE Users SET page = ? WHERE id = ?', (1, user_id))


def new_user(user_id):
    with sq.connect('users.db') as con:
        cursor = con.cursor()

        cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))

        if cursor.fetchall():
            return

        cursor.execute(f'INSERT INTO Users (id, page) VALUES ({user_id}, 3)')


def page_user(user_id):
    with sq.connect('users.db') as con:
        cursor = con.cursor()

        cursor.execute('SELECT page FROM Users WHERE id = ?', (user_id,))

        return cursor.fetchall()[0][0]


def bookmarks_user(user_id):
    with sq.connect('users.db') as con:
        cursor = con.cursor()

        cursor.execute('SELECT * FROM UsersBookmarks WHERE id = ?', (user_id,))

        return set(map(lambda x: x[1], cursor.fetchall()))


def change_user_page(user_id, change_page):
    with sq.connect('users.db') as con:
        cursor = con.cursor()

        cursor.execute('UPDATE Users SET page = ? WHERE id = ?', (change_page, user_id))


def add_user_bookmarks(user_id, page_book):
    with sq.connect('users.db') as con:
        cursor = con.cursor()

        cursor.execute('INSERT INTO UsersBookmarks (id, bookmark) VALUES (?, ?)', (user_id, page_book))


with sq.connect('users.db') as con:
    cursor = con.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, page INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS UsersBookmarks (id INTEGER, bookmark INTEGER)''')

    cursor.execute('''INSERT INTO Users (id, page) VALUES (12, 2)''')

    con.commit()








