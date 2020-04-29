import random
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from .users import User
from .chats import Chat


def gencode():
    return ''.join(chr(random.randint(ord('a'), ord('z'))) for _ in range(40))


# noinspection PyUnresolvedReferences
class ChatInvite(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'chat_invitations'

    chat_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('chats.id'), nullable=False, primary_key=True)
    code = sqlalchemy.Column(sqlalchemy.String,
                             index=True, default=gencode, nullable=True)
    chat = orm.relation('Chat')
