from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
import config

app = Flask(__name__)
app.config.from_object(config.Config)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


def init():
    import routes
    import apis
    from data import db_session
    from data.__all_models import Message, Chat, User
    db_session.global_init("db/bnet.sqlite")

    session = db_session.create_session()
    # user = User(username='test', email='test@test.com')
    # user.set_password('test_password')
    # session.add(user)
    # chat = Chat(title='test chat')
    # session.add(chat)
    # chat = session.query(Chat).get(1)
    # user = session.query(User).get(1)
    # chat.users.append(user)
    # message = Message(text='test message', user=user, chat=chat)
    # session.add(message)
    # message = user.chats[0].messages[0]
    # message.text = 'edited test message'
    # message = session.query(Message).get(1)
    session.commit()


init()

if __name__ == '__main__':
    app.run()
