from data import db_session
from data import Chat, User, Message, ChatInvite
from data.chat_invitations import gencode
from exceptions import LocalApi
import sqlalchemy.exc


def check_user_in_chat(chat_id, user_id):
    session = db_session.create_session()
    chat = session.query(Chat).get(chat_id)
    if chat is None:
        raise LocalApi.NotFoundError('chat not found')
    if session.query(User).get(user_id) not in chat.users:
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


def add_user(chat_id, user_id, notify=True):
    session = db_session.create_session()
    chat = session.query(Chat).get(chat_id)
    user = session.query(User).get(user_id)
    chat.users.append(user)
    session.commit()
    if notify:
        send_message(user_id, chat_id, "Присоединился(-ась) по ссылке-приглашению")


def new_chat(title, owner_user_id):
    session = db_session.create_session()
    user = session.query(User).get(owner_user_id)
    chat = Chat(title=title)
    session.add(chat)
    session.commit()
    add_user(chat.id, user.id, notify=False)
    send_message(user.id, chat.id, 'Чат создан')
    return chat


def check_invitation(user_id, code):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    invitation: ChatInvite = session.query(ChatInvite).filter(ChatInvite.code == code).first()
    if invitation is None:
        raise LocalApi.InvalidCode('no invitation with this code')
    chat = invitation.chat
    add_user(chat.id, user.id)
    session.commit()
    return chat.id


def create_invitation(user_id, chat_id):
    check_user_in_chat(chat_id, user_id)
    session = db_session.create_session()
    invitation = session.query(ChatInvite).get(chat_id)
    if invitation is not None:
        return invitation.code
    invitation = ChatInvite(chat_id=chat_id)
    session.add(invitation)
    session.commit()
    return invitation.code


def reset_invitation(user_id, chat_id):
    check_user_in_chat(chat_id, user_id)
    session = db_session.create_session()
    invitation: ChatInvite = session.query(ChatInvite).get(chat_id)
    if invitation is None:
        raise LocalApi.NotFoundError
    invitation.code = gencode()
    session.commit()
    return invitation.code
