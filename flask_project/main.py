import math
import re
import sqlite3
from app import app
import time
from flask import Flask, url_for, render_template, request, flash, g, session, \
    make_response, redirect, abort, jsonify  # pip install Flask , обработчик шаблонов
import sqlite3 as sq3
import os
from DB import open_close_db
import DB
from werkzeug.security import generate_password_hash, check_password_hash
"""работа с авторизацией"""
from flask_login import LoginManager, login_user, login_required, current_user, logout_user , \
    UserMixin
from forms import LoginForm
from admin.admin import admin

DATABASE = '/tmp/flask.db'
DEBUG = True
MAX_CONTENT_LENGTH = 1024 * 1024 * 10
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'dawdadjadkjalkdalkdjlakjd'
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flask.db')))
app.register_blueprint(admin,url_prefix='/admin')

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для доступа к странице'
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


class UserLogin(UserMixin):
    # from_db create формируют свойство __user

    # используется в декораторе userloader
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    # def is_authenticated(self):  usermixin уже имеет эти методы
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False

    def get_id(self):
        return str(self.__user['id'])

    def getName(self):
        return self.__user['name'] if self.__user else "Без имени"

    def getEmail(self):
        return self.__user['email'] if self.__user else "Без email"

    def getAvatar(self, app):
        img = None
        if not self.__user["avatar"]:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию"+ str(e))
        else:
            img = self.__user['avatar']

        return img

    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1] #разделяем название файла
        if ext == "png" or ext == "PNG":
            return True
        return False


def connect_db():
    conn = sq3.connect(app.config['DATABASE'])
    conn.row_factory = sq3.Row
    return conn


# open_close_db()

menus = [{"name": "Установка", "url": "install-flask"},
         {"name": "Первое приложение", "url": "first_app"},
         {"name": "Обратная связь", "url": "contact"},
         {"name": "О сайте", "url": "about"},
         {"name":"Админка","url":"admin"}
         ]
dbase = None


@app.before_request
def before_request():
    """Установление с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDatabase(db)


def get_db():
    """Cоединение с БД, если оно еще не установлено"""
    if not hasattr(g, 'link_db'):  # ищет свойство link.db
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.route('/first_app')
def first():
    return render_template('first_app.html', title='Первое приложение', menus=menus, menu=dbase.getMenu())


class FDatabase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = """SELECT * FROM mainmenu"""
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")

        return []

    def addPost(self, title, text, url):  # ф-ии добавления зн-й в БД
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM post WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Cтатья с таким url уже существует")
                return False  # фу-я addpost возвращает false и  дальше не пойдет
            base = url_for('static', filename='images.html')
            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                          "\\g<tag>" + base + "/\\g<url>",
                          text)
            tm = math.floor(time.time())
            self.__cur.execute('Insert INTO post VALUES(NULL,?,?,?,?)', (title, text, url, tm))
            self.__db.commit()  # cохраняет в бд
        except sq3.Error as e:
            print("Ошибка доб" + str(e))
            return False

        return True

    def getFeedBack(self, name, email, txt):
        try:
            self.__cur.execute('Insert INTO feedback VALUES(NULL,?,?,?)', (name, email, txt))
            res = self.__cur.fetchone()
            self.__db.commit()  # cохраняет в бд
        except sq3.Error as e:
            print("Ошибка доб" + str(e))
            return False

        return True

    def getPost(self, alias):  # ф-ии вытаскивания зн-й из БД
        try:
            self.__cur.execute(f"SELECT title, text  FROM post WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sq3.Error as e:
            print("Ошибка получения статьи из БД" + str(e))

        return (False, False)

    def getPostsAnounce(self):  # ф-ии вытаскивания зн-й из БД
        try:
            self.__cur.execute(f'SELECT id, title, text, url FROM post ORDER by time DESC')
            res = self.__cur.fetchall()
            if res: return res
        except sq3.Error as e:
            print("Ошибка получения статьи" + str(e))

        return []

    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE'{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL,?,?,?,NULL,?)", (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД" + str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))

        return False

    def DeletePost(self, post_id):
        try:
            self.__cur.execute('DELETE FROM post WHERE id = ?', (post_id))
            self.__db.commit()
        except sq3.Error as e:
            print("Ошибка доб" + str(e))
            return False


    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sqlite3.Binary(avatar) #преобразуем аватарку в бинарные днны
            self.__cur.execute(f"UPDATE users set avatar = ? WHERE id= ?", (binary,user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ощибка обновления аватара в БД" + str(e))
            return False
        return True


# Cоздание ответа с помощью кортежей
# (responce,status,headers) status-номер ошибки headers-заголовки
# (responce,headers)
# (responce,status)


@app.errorhandler(404)
def pageNot(error):
    return ("Страница не найдена", 404)


@app.route("/index")  # Создаем каталог templates где будут храниться наши html
@app.route("/")  # Возвращает index при обращении к URL / , /index
def index():
    db = get_db()  # поиск бд
    dbase = FDatabase(db)  # подсоединение к бд fdatabase
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    content = render_template("index.html", menu=dbase.getMenu(), menus=menus, posts=dbase.getPostsAnounce(),
                              visits=session['visits'])

    # print(url_for('index'))
    # res = make_response(content) #формируем ответ сервера
    # res.headers['Content-Type'] = 'text/plain' # отображение контента не HTML, а текстом с тегами
    # res.headers['Server'] = 'flasksite'
    return content, 200, {'Content-Type': 'text/html'}


@app.teardown_appcontext  # срабатывает когда происходить уничтожение контекста приложения
def close_db(g):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/get-message")
def get_message():
    return jsonify(
        message="1323 json message",
        date="12.12.12",
        id=10,
    )


@app.route("/about")
def about():
    return render_template("about.html", title="Инфо о сайте", menus=menus, menu=dbase.getMenu())


@app.route("/news")
def news():
    return render_template("news.html", title="Новости", menu=dbase.getMenu(), menus=menus)


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    if request.method == "POST":  # происходит считывание информации с HTML страницы параметров name post
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash("Ошибка добавления статьи", category='error')
            else:
                flash("Cтатья отправлена успешно", category='success')
        else:
            flash("Ошибка добавления статьи", category='error')

    return render_template('add_post.html', menu=dbase.getMenu(), title="Добавление статьи", menus=menus)


@app.route("/post/<alias>")
@login_required
def showPost(alias):
    title, \
    post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)


# @app.route('/profile/<username>')
# def profile_user(username):
#     db = get_db()
#     dbase = FDatabase(db)
#     id=dbase.getPostsAnounce(request.form['id'])
#     return render_template("user.html",id=id, title="Пользователь", username=username, menu=dbase.getMenu())

@app.route('/profile')
@login_required
def profile():
    db = get_db()
    dbase = FDatabase(db)
    return render_template("profile.html", menus=menus, menu=dbase.getMenu(), title="Профиль")

    # f'''<p><a href="{url_for('logout')}">Выйти из профиля </a>
    #            <p>user info:{current_user.get_id()}''' #cпециальная глобальная переменная для отображения id


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта")
    # return redirect(url_for('login')) # перенаправляет на логин
    return render_template("logout.html", menus=menus, menu=dbase.getMenu(), title="Профиль")


@app.route('/contact', methods=["POST", "GET"])
def contact():
    db = get_db()
    dbase = FDatabase(db)
    # быстрые сообщения flash  и секретный ключ
    if request.method == 'POST':
        res = dbase.getFeedBack(request.form['name'], request.form['email'], request.form['txt'])
        if res:
            flash("Мы рассмотрим ваш вопрос")
            #return redirect(url_for('index'))
        else:
            flash("Ошибка отправки")
        # print(request.form)
    return render_template('contact.html', title="Обратная связь", menus=menus, menu=dbase.getMenu())


# куки
# set_cookie(key,value="",max_age=NOne)
# value-данные хранимые в cookies
# max_age аргумент , указывающий предельное время хранения в браузере клиента

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    # проверяет метод post
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['psw'],form.psw.data):
            userlogin = UserLogin().create(user)
            """Кнопка запомнить меня"""
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Неверная пара логин/пароль", "error")
    return render_template('login.html', menus=menus, menu=dbase.getMenu(), title='Авторизация', form=form)
    # if request.method == "POST":
    #     user = dbase.getUserByEmail(request.form['email'])
    #     if user and check_password_hash(user['psw'], request.form['psw']):
    #         userlogin = UserLogin().create(user)
    #         """Кнопка запомнить меня"""
    #         login_user(userlogin)
    #         rm =True if request.form.get('remainme') else False
    #         return redirect(url_for('index'))
    #
    #         # args.get. получает значение next= в URL
    #         return redirect(request.args.get("next") or url_for("profile"))
    #
    #     flash("Неверная пара логин/пароль", "error")
    # return render_template('login.html', menus=menus, menu=dbase.getMenu(), title='Авторизация')


#   log = ''
#   if request.cookies.get('logging'):  # ищем значение по ключу
#       log = request.cookies.get('logging')

#   res = make_response(render_template('login.html', log=log, menus=menus, menu=dbase.getMenu(), title='Авторизация'))
#   res.set_cookie("logging", "yes", 10)  # при повторном обращении получаем yes
#   return res

@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash("Ошибка добавлния аватара", "error")
                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("ошибка обновы", "Error")

    return redirect(url_for('profile'))


@app.route("/userava")
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":  # ищет значение в HTML
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 and len(request.form['psw']) > 4 and \
                request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрированы")
                return redirect(url_for('login'))
            else:
                flash("Ошибка добавления в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")
    return render_template('register.html', title="Регистрация", menus=menus, menu=dbase.getMenu())


# @app.route("/logout")
# def logout():
#     res = make_response("<p>Вы больше не авторизованы<p>")
#     res.set_cookie("logging", "", 0)
#     return res


# with app.test_request_context():
#     print(url_for('about'))


if __name__ == "__main__":
    app.run(debug=True)
