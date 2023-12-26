from datetime import datetime
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<users {self.id}>"


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profile {self.id}>"

@app.route("/new_index")
@app.route("/")
def new_index():
    return render_template("new_index.html", title="Главная")


@app.route('/new_register', methods=("post", "get"))
def new_register():
    if request.method == "POST":
        try:
            hash = generate_password_hash(request.form['psw'])
            u = Users(email=request.form['email'], psw=hash)  # красным параметры бд
            db.session.add(u)
            db.session.flush()  # перемещение записи в таблицу

            p = Profiles(name=request.form['name'], old=request.form['old'],
                         city=request.form['city'], user_id=u.id)
            db.session.add(p)
            db.session.commit()  # меняет бд и сохраняет изменения в таблицах

        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
    return render_template("new_register.html", title="Регистр")


if __name__ == "__main__":
    app.run(debug=True)
