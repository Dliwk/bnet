from data import db_session
from data import Chat
from exceptions import LocalApi


def get_chat(chat_id):
    session = db_session.create_session()
    chat = session.query(Chat).get(chat_id)
    if chat is None:
        raise LocalApi.NotFoundError('chat not found')
    return chat
