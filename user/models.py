from counterfeit_ic import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80))
    email = db.Column(db.String(35), unique=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(60))
    creation_date = db.Column(db.DateTime)
    is_approved = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_contributor = db.Column(db.Boolean, default=False)

    # user = User(fullname='sunil', username='sunilzs', email='sunil@gmail.com', password='hello123', is_approved=True, is_admin=True, is_contributor=True)
    # INSERT INTO User ('sunil', 'sunilzs', 'sunil@gmail.com', 'hello123','2018-12-04 03:29:41', 1, 1, 1)
    def __init__(self, fullname, email, username, password,is_approved=False, is_admin=False, is_contributor=False):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.creation_date = datetime.utcnow()
        self.is_approved = is_approved
        self.is_admin = is_admin
        self.is_contributor = is_contributor

    def __repr__(self):
        return '<User %r>' % self.username


# class PWHash(db.Model):
#     __tablename__ = 'pwhash'
#     id = db.Column(db.Integer, primary_key=True)
#     user_email = db.Column(db.String(35), unique=False)
#     code = db.Column(db.String(256))
#     generated_date = db.Column(db.DateTime)

#     def __init__(self, email, code):
#         self.user_email = email
#         self.code = code
#         self.generated_date = datetime.utcnow()
