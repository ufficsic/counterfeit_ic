from counterfeit_ic import db
from datetime import datetime


class Dataset(db.Model):
    __tablename__ = 'dataset'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    description = db.Column(db.String(256))
    filename = db.Column(db.String(80))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_date = db.Column(db.DateTime)


    def __init__(self, name, description, filename, user_id):
        self.name = name
        self.description = description
        self.filename = filename
        self.user = user_id
        self.creation_date = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.filename