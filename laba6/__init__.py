from flask import Flask
from laba6.config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Session(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['database'] = db

with app.app_context():

    from laba6.review.blueprint import reviews

    app.register_blueprint(reviews, url_prefix='/reviews')

    from laba6.auth import blueprint

    app.register_blueprint(blueprint.auth, url_prefix='/auth')

from laba6.routes import *
from laba6.logout import *
