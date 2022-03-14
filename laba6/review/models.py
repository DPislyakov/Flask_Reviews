from flask import current_app

myapp = current_app

with myapp.app_context():
    db = current_app.config.get('database')


class ReviewCin(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	nameofCinema = db.Column(db.String(128), index=True)
	text = db.Column(db.UnicodeText)
	rating = db.Column(db.Integer)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Cinema(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nameCinema = db.Column(db.String(128), index=True)
	author = db.Column(db.String(128), index=True)
	firstPublic = db.Column(db.Date)


class RatingReview2(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_cinema = db.Column(db.Integer, index=True)
	good = db.Column(db.String(52), index=True)
	kom = db.Column(db.String(128), index=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
