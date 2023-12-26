import sqlite3 as sq3
import os



def create_db():
    sq3.connect('flask.db')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "flask.db")


# c = db.cursor()  # Позволяет работать с БД
# c.execute("""DROP TABLE books""")
def open_close_db():
    with  sq3.connect(db_path) as db:
        c = db.cursor()
        #c.execute("""DROP TABLE books""")

        c.execute("""CREATE TABLE IF NOT EXISTS mainmenu(
        id integer PRIMARY KEY AUTOINCREMENT,
        title text,
        url text
        )
        """)
        c.execute("""CREATE TABLE IF NOT EXISTS post(
        id integer PRIMARY KEY AUTOINCREMENT,
        title text NOT NULL,
        text text NOT NULL,
        url text NOT NULL,
        time integer NOT NULL
        )
        """)
        c.execute("""CREATE TABLE IF NOT EXISTS users(
        id integer PRIMARY KEY AUTOINCREMENT,
        name text NOT NULL,
        email text NOT NULL,
        psw text NOT NULL,
        avatar BLOB DEFAULT NULL, 
        time integer NOT NULL
        )
        """)
        #avatar - аватарка пользователя
        c.execute("""CREATE TABLE IF NOT EXISTS feedback(
                id integer PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL,
                email text NOT NULL,
                txt
                )
                """)





        #c.execute("""DROP TABLE users""")
        # c.execute("INSERT INTO mainmenu VALUES('1','Главная','\ ')")
        #c.execute("""UPDATE mainmenu SET url='/add_post' WHERE id=2""")
        # c.execute("INSERT INTO mainmenu VALUES('2','Добавить статью','add_post')")
        #c.execute("INSERT INTO mainmenu VALUES('3','Авторизация','/login')")
        #c.execute("""UPDATE mainmenu SET url='/' WHERE id=1""")
        db.commit()

open_close_db()
