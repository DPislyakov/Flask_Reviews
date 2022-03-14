import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class DevConfig(object):
	DEBUG = True
	CSRF_ENABLED = True
	SECRET_KEY = "my-secret-key"
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SESSION_TYPE = 'filesystem'
	
