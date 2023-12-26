import sqlite3

from flask import Blueprint, request, redirect, url_for, render_template, flash, session, g



admin = Blueprint("admin", __name__, template_folder='templates', static_folder='static')

menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.listusers', 'title': 'Список пользователей'},
        {'url': '.listpubs', 'title': 'Список статей'},
        {'url': '.logout', 'title': 'Выйти'}]

db = None


@admin.before_request
def before_request():
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@admin.route('/list_users')
def listusers():
    if not islogged():
        return redirect(url_for('.login'))

    list = []

    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, email FROM users ORDER by time DESC")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка БД" + str(e))
    return render_template('admin/list_users.html', title='Cписок пользователей', menu=menu, list=list)


@admin.route('/list_pubs', methods=["POST", "GET"])
def listpubs():
    if not islogged():
        return redirect(url_for('admin.login'))

    post_list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute("SELECT id, title, text, url FROM post")
            post_list = cur.fetchall()

            if request.method == "POST":
                post_id = request.form.get('post_id')
                if post_id:
                    cur = db.cursor()
                    cur.execute('DELETE FROM post WHERE id = ?', (post_id))
                    db.commit()
                    return redirect(url_for('admin.listpubs'))

        except sqlite3.Error as e:
            print("Ошибка получения из БД" + str(e))

    return render_template('admin/list_pubs.html', title="Список статей", menu=menu, list=post_list)


@admin.route('/')
def index():
    if not islogged():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', menu=menu, title="Aдмин-панель")


def login_admin():
    session['admin_logged'] = 1


def islogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/login', methods=["POST", "GET"])
def login():
    if islogged():
        return redirect(url_for('.index'))

    if request.method == 'POST':
        if request.form['user'] == "admin" and request.form['psw'] == '123456':
            login_admin()
            return redirect(url_for('admin.index'))  # точка ведет к функции индекс админа
        else:
            flash("Неверная пара логин пароль", "error")
    return render_template("admin/login.html", title="Admin-panel")


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not islogged():
        return redirect(url_for('.login'))
    logout_admin()

    return redirect(url_for('.login'))
