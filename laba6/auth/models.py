from werkzeug.security import generate_password_hash, check_password_hash

from flask import current_app
from flask_login import UserMixin

myapp = current_app

with myapp.app_context():
    db = current_app.config.get('database')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    pass_hash = db.Column(db.String(256))
    articles = db.relationship('ReviewCin', backref='author')
    articls = db.relationship('RatingReview2', backref='author')

    def set_pass(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_pass(self, password):
        return check_password_hash(self.pass_hash, password)

    def __repr__(self):
        return f"{self.name}"
