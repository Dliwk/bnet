from data import db_session
from data import User
from exceptions import LocalApi


def register(username, password):
    session = db_session.create_session()
    user = session.query(User).filter(User.username == username).first()
    if user:
        raise LocalApi.DuplicateError(f'User with this username already exists: "{username}"', duptype='username')

    if len(password) < 5:
        raise LocalApi.PasswordError('This password is too simple')

    user = User(username=username)
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


def get_user_public_info(user_id=None, username=None):
    if username is None and user_id is None:
        raise LocalApi.InvalidCall('no one from username and user_id set')
    session = db_session.create_session()
    user: User
    if user_id is not None:
        user = session.query(User).get(user_id)
    else:
        user = session.query(User).filter(User.username == username).first()
    if user is None:
        raise LocalApi.NotFoundError
    return User(
        id=user.id,
        username=user.username,
        fullname=user.fullname,
        about=user.about,
        background_image_url=user.background_image_url)


def edit_profile(user_id, fullname, about, background_image_url):
    session = db_session.create_session()
    user: User = session.query(User).get(user_id)
    if user is None:
        raise LocalApi.NotFoundError
    user.fullname = fullname
    user.about = about
    user.background_image_url = background_image_url
    session.commit()
