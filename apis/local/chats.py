from data import db_session
from data import Chat, User, Message
from exceptions import LocalApi


def get_chat(chat_id):
    session = db_session.create_session()
    chat = session.query(Chat).get(chat_id)
    if chat is None:
        raise LocalApi.NotFoundError('chat not found')
    return chat


def send_message(user_id, chat_id, text):
    session = db_session.create_session()
    message = Message(user_id=user_id, chat_id=chat_id, text=text)
    session.add(message)
    session.commit()
