import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


# noinspection PyUnresolvedReferences
class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    send_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                  default=datetime.datetime.now, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)

    chat_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("chats.id"), nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"), nullable=False)
    is_system = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)
    user = orm.relation('User')
    chat = orm.relation('Chat')

    def __repr__(self):
        return f'<Message id={self.id} text={self.text}>'
