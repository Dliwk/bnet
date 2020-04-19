from data import db_session
from data import User
from exceptions import LocalApi


def register(username, email, password):
    session = db_session.create_session()
    user = session.query(User).filter(User.username == username).first()
    if user:
        raise LocalApi.DuplicateError(f'User with this username already exists: "{username}"', duptype='username')
    user = session.query(User).filter(User.email == email).first()
    if user:
        raise LocalApi.DuplicateError(f'User with this email already exists: "{email}"', duptype='username')

    if len(password) < 5:
        raise LocalApi.PasswordError('This password is too simple')

    user = User(username=username,
                email=email)
    user.set_password(password)
    session.add(user)
    session.commit()


def get_user_for_login(password, username=None, email=None):
    if not username and not email:
        raise LocalApi.InvalidCall('no email or username passed')
    if username and email:
        raise LocalApi.InvalidCall('email and username passed together')

    session = db_session.create_session()
    if email:
        user = session.query(User).filter(User.email == email).first()
    else:  # username:
        user = session.query(User).filter(User.username == username).first()

    if not user:
        raise LocalApi.NoUserError('no user with this email or username')

    if not user.check_password(password):
        raise LocalApi.InvalidPasswordError('invalid password')

    return user
