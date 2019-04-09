from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail
from flask_migrate import Migrate
from flask_uploads import UploadSet, ARCHIVES, IMAGES, configure_uploads
import os, sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append('/home/cic/counterfeit_ic')

import settings as settings

app = Flask(__name__)
app.config.from_object(settings)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = ''

from user import models
User = models.User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

archives = UploadSet('archives', ARCHIVES)
pimage = UploadSet('photos', IMAGES)
pspec = UploadSet('pdf', extensions=('pdf'))
configure_uploads(app, (archives, pimage, pspec))


from user.views import *
from inventory.views import *
from inventoryView.views import *
from dataset.views import *
from home.views import *
from contact.views import *
from resources.views import *
from taxonomy.views import *
from instructions.views import *

import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(filename='/var/log/FlaskLogs/test.log',level=logging.DEBUG)
logging.info(pimage)
logging.info(os.path.join(app._static_folder, 'static', 'images', 'product_images'))
logging.info(os.path.join('/home/cic/counterfeit_ic', app._static_folder, 'static', 'images', 'product_images'))
logging.info(app._static_folder)

if __name__ == '__main__':
    app.run()
