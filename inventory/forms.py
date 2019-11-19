from counterfeit_ic import pimage, pspec, archives
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, validators, StringField, SelectField, IntegerField


class CreateComponentsForm(FlaskForm):
    manufacturer = StringField('Manufacturer Name', [validators.Required()])
    product = StringField('Product Name', [validators.Required()])
    pspec = FileField('Product Specification', validators=[
        FileRequired(),
        FileAllowed(pspec, 'PDFs only!')
    ])
    pimage = FileField('Product Image', validators=[
        FileRequired(),
        FileAllowed(pimage, 'Images only!')
    ])
    total_samples = IntegerField(
        'Total Samples Tested', [validators.Required()])
    archive = FileField('Upload Components', validators=[
        FileRequired(),
        FileAllowed(archives, 'ZIP Files only!')
    ])
    submit = SubmitField('Submit')


class AddComponentsForm(FlaskForm):
    archive = FileField('Upload Components', validators=[
        FileRequired(),
        FileAllowed(archives, 'ZIP Files only!')
    ])
    total_samples = IntegerField(
        'Total Samples Tested', [validators.Required()])
    submit = SubmitField('Submit')


class EditProductForm(FlaskForm):
    product = StringField('Product Name', [validators.Required()])
    pspec = FileField('Product Specification', validators=[
        FileAllowed(pspec, 'PDFs only!')
    ])
    pimage = FileField('Product Image', validators=[
        FileAllowed(pimage, 'Images only!')
    ])
    total_samples = IntegerField('Total Samples Tested', [
                                 validators.Required()])
    submit = SubmitField('Submit')
