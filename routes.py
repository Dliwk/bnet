from flask import render_template, redirect, url_for
from app import app
from forms import LoginForm, RegisterForm
from apis.local import account
import apis.local as api
from exceptions import LocalApi
from flask_login import login_required, logout_user


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('chats'))
    # return render_template('index.jinja2', title='Главная страница', user={})


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        account.login(username=form.username.data, password=form.password.data)
        return redirect(url_for('index'))
    return render_template('login.jinja2', title='Авторизация', form=form)


@app.route('/chats')
def chats():
    return render_template('chats.jinja2', title='Чаты')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_confirm.data:
            return render_template('register.jinja2', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        try:
            account.register(form.username.data,
                             form.email.data,
                             form.password.data)
        except LocalApi.DuplicateError as e:
            if e.duptype == 'email':
                duptype = 'email'
            elif e.duptype == 'username':
                duptype = 'логином'
            else:
                duptype = 'неопределенно'
            return render_template('register.jinja2', title='Регистрация',
                                   form=form,
                                   message="Пользователь с таким " + duptype + " уже есть")
        except LocalApi.PasswordError:
            return render_template('register.jinja2', title='Регистрация',
                                   form=form,
                                   message="Ваш пароль слишком простой")
        else:
            return redirect(url_for('login'))
    return render_template('register.jinja2', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/chat/<int:chat_id>')
def chat(chat_id):
    selected_chat = None
    try:
        selected_chat = api.chats.get_chat(chat_id)
    except LocalApi.NotFoundError:
        return render_template('not_found.jinja2')
    return render_template('chat.jinja2', chat=selected_chat)
