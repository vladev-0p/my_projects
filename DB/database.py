import sqlite3 as sq3
import os.path

#sq3.connect('user.db')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "user.db")


# c = db.cursor()  # Позволяет работать с БД
# c.execute("""DROP TABLE books""")
with  sq3.connect(db_path) as db:
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS books (
    name text,
    viewses integer,
    author text
    )
    """)

    #добавление записи

    #c.execute("INSERT INTO books VALUES('Master i Margarita',350,'Bulgakov')")
    # c.execute("INSERT INTO books VALUES('Onegin',350,'Pushkin')")
    # # c.execute("INSERT INTO books VALUES('Master i Margarita',350,'Bulgakov')")
    c.execute("INSERT INTO books VALUES('petrov',350,'ivanov')")
    #
    c.execute("SELECT rowid, * FROM books ")
    #
    items= c.fetchall()
    print(c.fetchmany(2)) # 2 записи
    #print(c.fetchone()[2])
    for el in items:
        print(str(el[0])+" "+str(el[1])+" "+ str(el[2]))
    #DELETE duplicates
    # c.execute(
    # """DELETE FROM books
    # WHERE    rowid not in
    #          (
    #          select  min(rowid)
    #          from    books
    #          group by name
    #          ,       viewses
    #          ,       author
    #          )
    # """)
    # #UPDATEE data
    # c.execute("UPDATE books SET viewses=1500 WHERE author = 'Bulgakov' ")
    # c.execute("DELETE FROM books")

    #Delete data
    c.execute("DELETE FROM books WHERE rowid = 1 ")

    #c.execute("DELETE FROM books WHERE name = 'Master i Margarite' ")


    db.commit()


#

