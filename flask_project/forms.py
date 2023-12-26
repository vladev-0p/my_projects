from flask_wtf import FlaskForm
from wtforms import StringField ,SubmitField,BooleanField,PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[Email("Некорректный Email")])
    psw = PasswordField("Пароль:", validators=[DataRequired(), Length(min=4, max=12, message="Длина пароля должна быть от 4 до 12 символов")])
    remember= BooleanField("Запомнить", default=False)
    submit= SubmitField("Войти")
