from counterfeit_ic import pimage, pspec, archives
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, validators, StringField, SelectField

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
    submit = SubmitField('Submit')


class EditProductForm(FlaskForm):
    # manufacturer = SelectField(
    #     label = 'Manufacturer Name', 
    #     [validators.Required()]
    # )
    product = StringField('Product Name', [validators.Required()])
    pspec = FileField('Product Specification', validators=[
        # FileRequired(),
        FileAllowed(pspec, 'PDFs only!')
    ])
    pimage = FileField('Product Image', validators=[
        # FileRequired(),
        FileAllowed(pimage, 'Images only!')
    ])
    submit = SubmitField('Submit')