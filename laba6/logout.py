from . import app
from flask import url_for, redirect
from flask_login import logout_user,login_required


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main_page'))