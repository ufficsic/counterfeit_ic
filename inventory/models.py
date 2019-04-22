from counterfeit_ic import db, ma
from user.models import User
from datetime import datetime


class Manufacturer(db.Model):
    __tablename__ = 'manufacturer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Manufacturer %r>' % self.name.capitalize()


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    spec_file_name = db.Column(db.String(80))
    spec_image_name = db.Column(db.String(80))
    manufacturer = db.Column(db.Integer, db.ForeignKey('manufacturer.id'))
    is_approved = db.Column(db.Boolean, default=False)

    def __init__(self, name, manufacturer_id, spec_file_name=None, spec_image_name=None, is_approved=False):
        self.name = name.lower()
        self.manufacturer = manufacturer_id
        self.spec_file_name = spec_file_name
        self.spec_image_name = spec_image_name
        self.is_approved = is_approved

    def __repr__(self):
        return '<Product %r>' % self.name.capitalize()


class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product


class DefectType(db.Model):
    __tablename__ = 'defect_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    primary_type = db.Column(db.String(80))
    secondary_type = db.Column(db.String(80))
    # is_approved = db.Column(db.Boolean, default=False)

    def __init__(self, name, primary_type, secondary_type):
        self.name = name.lower()
        self.primary_type = primary_type
        self.secondary_type = secondary_type

    def __repr__(self):
        return '<DefectType %r>' % self.name.capitalize()


class DefectTypeSchema(ma.ModelSchema):
    class Meta:
        model = DefectType


class Defect(db.Model):
    __tablename__ = 'defect'
    id = db.Column(db.Integer, primary_key=True)
    chip = db.Column(db.Integer, db.ForeignKey('chip.id'))
    sample = db.Column(db.Integer, db.ForeignKey('sample.id'))
    defect_type = db.Column(db.Integer, db.ForeignKey('defect_type.id'))
    defect_image_name = db.Column(db.String(80))
    creation_date = db.Column(db.DateTime)

    def __init__(self, chip_id, sample_id, defect_type_id, defect_image_name):
        self.chip = chip_id
        self.sample = sample_id
        self.defect_type = defect_type_id
        self.defect_image_name = defect_image_name
        spec_image_name = db.Column(db.String(80))
        self.creation_date = datetime.utcnow()

    def __repr__(self):
        return '<Defect %r>' % self.id


class Sample(db.Model):
    __tablename__ = 'sample'
    id = db.Column(db.Integer, primary_key=True)
    chip = db.Column(db.Integer, db.ForeignKey('chip.id'))
    # sample_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    is_approved = db.Column(db.Boolean, default=True)

    def __init__(self, chip_id):
        self.chip = chip_id
        self.creation_date = datetime.utcnow()

    def __repr__(self):
        return '<Sample %r>' % self.id


class Chip(db.Model):
    __tablename__ = 'chip'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    manufacturer = db.Column(db.Integer, db.ForeignKey('manufacturer.id'))
    is_approved = db.Column(db.Boolean, default=True)
    __table_args__ = (db.UniqueConstraint('user', 'product',
                                          'manufacturer', name='user_manufacturer_product'),)

    def __init__(self, user, manufacturer, product):
        self.user = user
        self.manufacturer = manufacturer
        self.product = product
        self.creation_date = datetime.utcnow()

    def __repr__(self):
        return '<Chip %r>' % self.id
