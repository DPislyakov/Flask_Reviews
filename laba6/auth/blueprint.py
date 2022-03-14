from .models import User
from flask import url_for, render_template, redirect, flash, Blueprint, current_app

from flask_login import login_user, login_required, current_user, LoginManager
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, SubmitField

auth = Blueprint('auth', __name__, url_prefix='/auth',template_folder='templates')

myapp = current_app

with myapp.app_context():
    db = current_app.config.get('database')

login_manager = LoginManager()
login_manager.init_app(myapp)


#Пример формы входа
class LoginForm(FlaskForm):
	name = StringField('Имя', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	submit = SubmitField("Войти")

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
# Тут поведение может быть различным.
# Текущая версия не отображает форму, если мы уже залогинились.
	if (current_user.is_authenticated):
		#flash(f"Вы уже ранее вошли как {current_user.name}")
		return redirect(url_for('auth.authwarning'))
	_form = LoginForm()
	if (_form.validate_on_submit()):
		username = _form.name.data
		password = _form.password.data
		user = User.query.filter_by(name = username).first()
		if (user and user.check_pass(password)):
			login_user(user)
			flash(f'Вы вошли на сайт как {username}')
			return redirect(url_for('main_page'))
		else:
			flash("Неверный пароль или логин")
	return render_template("login_page.html", form = _form)

@auth.route('/authwarning')
def authwarning():
    return render_template("authwarning.html",user=current_user.name)


class AddUserForm(FlaskForm):
	name = StringField('Имя', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	submit = SubmitField("Зарегистрировать пользователя")

@auth.route('/add_user', methods=['GET', 'POST'])
def add_user():
	_form = AddUserForm()
	if (_form.validate_on_submit()):
		u = User(name = _form.name.data)
# Обратите внимание,что это место изменено!
# Теперь мы храним пароль в хешированном виде
		u.set_pass(_form.password.data)
		db.session.add(u)
		db.session.commit()
		return redirect(url_for('auth.ready'))
	return render_template("add_user.html", form = _form)

@auth.route('/ready')
def ready():
    return render_template("ready.html")


@auth.route('/view_users')
@login_required
def view_users():
	_users = User.query.all()
	return render_template("view_users.html", users = _users)
