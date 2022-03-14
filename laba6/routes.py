#Импорт из текущего пакета -- там у нас экземпляр приложения.
from laba6 import app
from flask import render_template

#Используя app только здесь
@app.route('/')
def main_page():
	return render_template("main_page.html")

