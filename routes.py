from flask import render_template, redirect, url_for, request, jsonify, abort
from app import app
from forms import LoginForm, RegisterForm
import apis.local as api
from exceptions import LocalApi
from flask_login import login_required, logout_user, current_user, login_user
import sqlalchemy
import datetime
import time
from longpoll import notify_longpoll_requests, longpoll_waiters, Waiter


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('chats'))
    # return render_template('index.jinja2', title='Главная страница', user={})


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = api.account.get_user_for_login(username=form.username.data, password=form.password.data)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.jinja2', title='Авторизация', form=form)


@app.route('/chats/')
@login_required
def chats():
    return render_template('chats.jinja2', title='Чаты')


@app.route('/chats/new', methods=['POST'])
@login_required
def new_chat():
    title = request.args['title']
    created_chat = api.chats.new_chat(title=title, owner_user_id=current_user.id)
    return jsonify({'ok': True, 'chat_id': created_chat.id})


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_confirm.data:
            return render_template('register.jinja2', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        try:
            api.account.register(form.username.data,
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


@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
@login_required
def chat(chat_id):
    if request.method == 'GET':
        selected_chat = None
        try:
            selected_chat = api.chats.get_chat(chat_id, current_user.id)
        except LocalApi.NotFoundError:
            abort(404)
        except LocalApi.ForbiddenError:
            abort(403)
        try:
            return render_template('chat.jinja2', chat=selected_chat)
        except sqlalchemy.orm.exc.DetachedInstanceError:
            return chat(chat_id)  # без этого никак -- я не знаю почему это происходит, и почему только иногда

    elif request.method == 'POST':
        try:
            api.chats.send_message(user_id=current_user.id, chat_id=chat_id, text=request.values['text'])
        except LocalApi.ForbiddenError:
            abort(403)
        except LocalApi.NotFoundError:
            abort(404)
        else:
            return jsonify({'ok': True})


@app.route('/chat/<int:chat_id>/kick/<int:user_id>', methods=['POST'])
@login_required
def kick_member(chat_id, user_id):
    try:
        api.chats.kick_member(current_user.id, chat_id, user_id)
    except LocalApi.ForbiddenError:
        abort(403)
    except LocalApi.NotFoundError:
        abort(404)
    else:
        return jsonify({'ok': True})


@app.route('/chat/<int:chat_id>/updates', methods=['GET'])
@login_required
def get_chat_updates(chat_id):
    start_time = datetime.datetime.now()
    waiter = Waiter(user_id=current_user.id)
    longpoll_waiters.add(waiter)
    while datetime.datetime.now().timestamp() - start_time.timestamp() < 25 and not waiter.updates:
        time.sleep(0.1)
    longpoll_waiters.remove(waiter)
    return jsonify({'ok': True, 'values': waiter.updates})


@app.route('/join/<string:code>')
@login_required
def join_chat(code):
    chat_id: int
    try:
        chat_id = api.chats.check_invitation(current_user.id, code)
    except LocalApi.InvalidCode:
        abort(404)
    else:
        return redirect(f'/chat/{chat_id}')


@app.route('/invite/<int:chat_id>')
@login_required
def invite(chat_id):
    code: str
    try:
        code = api.chats.create_invitation(current_user.id, chat_id)
    except LocalApi.ForbiddenError:
        abort(403)
    except LocalApi.NotFoundError:
        abort(404)
    else:
        return render_template('invite_result.jinja2', code=code, chat_id=chat_id)


@app.route('/invite-reset/<int:chat_id>')
@login_required
def invite_reset(chat_id):
    code: str
    try:
        code = api.chats.reset_invitation(current_user.id, chat_id)
    except LocalApi.ForbiddenError:
        abort(403)
    except LocalApi.NotFoundError:
        abort(404)
    else:
        return render_template('invite_result.jinja2', code=code, chat_id=chat_id)


@app.route('/user/<string:username>')
def profile(username):
    try:
        return render_template('profile.jinja2',
                               user=api.account.get_user_public_info(username=username))
    except LocalApi.NotFoundError:
        abort(404)


@app.route('/profile/edit', methods=['POST', 'GET'])
@login_required
def profile_edit():
    if request.method == 'GET':
        return render_template('profile/edit.jinja2', user=current_user)
    else:
        api.account.edit_profile(current_user.id,
                                 fullname=request.values['fullname'].strip(), about=request.values['about'].strip(),
                                 background_image_url=request.values['background_image_url'].strip())
        return redirect(f'/user/{current_user.username}')


@app.route('/chat/<int:chat_id>/title/', methods=['POST', 'GET'])
@login_required
def edit_chat_title(chat_id):
    if request.method == 'GET':
        try:
            return render_template('edit_chat_title.jinja2', chat=api.chats.get_chat(chat_id, current_user.id))
        except LocalApi.NotFoundError:
            abort(404)
        except LocalApi.ForbiddenError:
            abort(403)
    else:
        try:
            api.chats.set_title(current_user.id, chat_id, request.values['title'])
        except LocalApi.ForbiddenError:
            abort(403)
        except LocalApi.NotFoundError:
            abort(404)
        else:
            return redirect(f'/chat/{chat_id}')
