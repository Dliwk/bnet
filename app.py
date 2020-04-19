from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
import config
from data import db_session, User
db_session.global_init("db/bnet.sqlite")

app = Flask(__name__)
app.config.from_object(config.Config)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


def init():
    import routes
    import apis
    import error_handlers


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


init()

if __name__ == '__main__':
    app.run()
