from flask_login import login_required, current_user
from flask import url_for, render_template, redirect, Blueprint, current_app

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DateField, ValidationError, BooleanField
from .models import Cinema, ReviewCin, RatingReview2

reviews = Blueprint('reviews', __name__, url_prefix='/reviews', template_folder='templates')

myapp = current_app

with myapp.app_context():
    db = current_app.config.get('database')


def my_length_check(__form, field):
    if len(field.data) > 128:
        raise ValidationError('Количество символов превосходит допустимый лимит в 128 символов')


class AddCinemaForm(FlaskForm):
    name = StringField('Название произведения', [DataRequired(), my_length_check])
    nameAuthor = StringField('Имя автора', [DataRequired(), my_length_check])
    date = DateField('Дата первой публикации', format='%Y-%m-%d')
    submit = SubmitField("Создать")


@reviews.route('/secondready')
def secondready():
    return render_template("ready2.html")


@reviews.route('/review/new', methods=['GET', 'POST'])
@login_required
def create_article():
    stron = []
    for row in range(len(Cinema.query.all())):
        stron.append(Cinema.query.all()[row].nameCinema)
    _form = AddReviewForm()
    _form.nameofCinema.choices = stron
    if (_form.validate_on_submit()):
        new_article = ReviewCin(nameofCinema=_form.nameofCinema.data, text=_form.text.data, rating=_form.rating.data,
                                author=current_user)
        # db.create_all()
        db.session.add(new_article)
        db.session.commit()
        # flash("Рецензия создана")
        return redirect(url_for('reviews.secondready'))
    return render_template("add_article.html", form=_form)


@reviews.route('/review/all', methods=['GET'])
def view_articles():
    _articles = ReviewCin.query.all()
    rat = []
    for row in range(len(RatingReview2.query.all())):
        rat.append(RatingReview2.query.all()[row].id_cinema)

    _rating = RatingReview2.query.all()

    return render_template("view_articles.html", articles=_articles, rating=_rating, rat=rat)


@reviews.route('/cinema/new', methods=['GET', 'POST'])
@login_required
def create_cinema():
    __form = AddCinemaForm()
    if (__form.validate_on_submit()):
        new_cinema = Cinema(nameCinema=__form.name.data, author=__form.nameAuthor.data, firstPublic=__form.date.data)
        db.session.add(new_cinema)
        db.session.flush()
        db.session.commit()
        # flash("Фильм добавлен")
        return redirect(url_for('reviews.secondready'))
    return render_template("add_cinema.html", form=__form)


@reviews.route('/cinema/all', methods=['GET'])
def view_cinemas():
    stron2 = []
    for row in range(len(ReviewCin.query.all())):
        stron2.append(ReviewCin.query.all()[row].id)
    print(stron2)

    _cinemas = Cinema.query.all()
    stron = []
    for row in range(len(Cinema.query.all())):
        stron.append(Cinema.query.all()[row].nameCinema)
    # print(stron)
    return render_template("view_cinema.html", articles=_cinemas)


class AddRatingReviewForm(FlaskForm):
    good = BooleanField('Рецензия была полезной', false_values='Рецензия не была полезной')
    kom = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField("Создать")


@reviews.route('/reviewrating/<id>/<name>/new', methods=['GET', 'POST'])
@login_required
def create_rr(id, name):
    # idreview = id

    _form = AddRatingReviewForm()
    _form.filmname = name
    # for row in range(len(ReviewCin.query.all())):
    # if ReviewCin.query.all()[row].id == idreview:
    # name = ReviewCin.query.all()[row].nameofCinema
    # _form.nameofCinema.choices = stron
    if (_form.validate_on_submit()):
        new_article = RatingReview2(id_cinema=id, good=_form.good.data, kom=_form.kom.data, author=current_user)
        db.create_all()
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('reviews.secondready'))
    return render_template("add_rr.html", form=_form)  # , name= name)


class AddReviewForm(FlaskForm):
    nameofCinema = SelectField(u'Выберите произведение')
    text = TextAreaField('Текст', validators=[DataRequired()])
    rating = SelectField(u'Выберите оценку', choices=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    submit = SubmitField("Создать")


class AddCinemaForm(FlaskForm):
    name = StringField('Название произведения', [DataRequired(), my_length_check])
    nameAuthor = StringField('Имя автора', [DataRequired(), my_length_check])
    date = DateField('Дата первой публикации', format='%Y-%m-%d')
    submit = SubmitField("Создать")
