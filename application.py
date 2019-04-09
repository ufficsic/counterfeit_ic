from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
import settings as settings

csrf = CsrfProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    db = SQLAlchemy(app)
    
    csrf.init_app(app)
    return app
