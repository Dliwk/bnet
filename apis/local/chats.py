from data import db_session
from data import Chat, User, Message
from exceptions import LocalApi


def check_user_in_chat(chat_id, user_id):
    session = db_session.create_session()
    if session.query(User).get(user_id) not in session.query(Chat).get(chat_id).users:
        raise LocalApi.ForbiddenError('chat not available for this user')


def get_chat(chat_id, user_id):
    check_user_in_chat(chat_id, user_id)
    session = db_session.create_session()
    chat = session.query(Chat).get(chat_id)
    if chat is None:
        raise LocalApi.NotFoundError('chat not found')
    return chat


def send_message(user_id, chat_id, text):
    check_user_in_chat(chat_id, user_id)
    session = db_session.create_session()
    message = Message(user_id=user_id, chat_id=chat_id, text=text)
    session.add(message)
    session.commit()


def new_chat(title, owner_user_id):
    session = db_session.create_session()
    user = session.query(User).get(owner_user_id)
    chat = Chat(title=title)
    chat.users.append(user)
    session.add(chat)
    session.commit()
    send_message(user.id, chat.id, 'Чат создан')
    return chat
