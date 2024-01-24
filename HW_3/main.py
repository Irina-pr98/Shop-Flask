'''
Создать форму для регистрации пользователей на сайте. 
Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться". 
При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.
'''

import hashlib

from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
import binascii
from forms import RegistrationForm
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///users2.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        dk = hashlib.pbkdf2_hmac(hash_name='sha256', password=bytes(password, 'utf-8'), salt=b'bad_salt', iterations=100000)

        password = binascii.hexlify(dk)
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('success.html', username=username, email=email)

    return render_template('register.html', form=form)


@app.route('/users/', methods=['POST', 'GET'])
def get_all_users():
    users = User.query.all()
    return f'{list(users)}'