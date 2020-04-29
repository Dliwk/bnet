import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from .users import User


# noinspection PyUnresolvedReferences
class Chat(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String,
                              nullable=False)
    users = orm.relation('User',
                         secondary='chats_to_users',
                         backref='users')
    messages = orm.relation('Message', back_populates='chat')

    def __repr__(self):
        return f'<Chat id={self.id} title={self.title}>'


# noinspection PyUnresolvedReferences
chats_to_users_table = sqlalchemy.Table(
    'chats_to_users', SqlAlchemyBase.metadata,
    sqlalchemy.Column('chats', sqlalchemy.Integer, sqlalchemy.ForeignKey('chats.id')),
    sqlalchemy.Column('users', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')))
