from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView


# APP config
app = Flask(__name__)


app.config['SECRET_KEY'] = '05534799c46abb445b8ed2650a4a963675bef384af4b57e8139424fb43ea423aeea48dc7ffeaf7f3a99a31bb4ae99b0f5858b8d7902dd0e84221475da58e4438'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'



#db set

db = SQLAlchemy(app)

#crypt method
bcrypt = Bcrypt(app)

#login session
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'


from mainblog import routes, admin


