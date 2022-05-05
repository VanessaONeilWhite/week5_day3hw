from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


#initializing stuff
app = Flask(__name__)
app.config.from_object(Config)

#register plugins
login = LoginManager(app)

#init my database manager
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#configure settings
login.login_view='login'
login.login_message = 'You must login to continue'
login.login_message_category = 'warning'

from app import routes, models