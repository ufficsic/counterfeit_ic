from counterfeit_ic import archives
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, StringField, validators

# archives = UploadSet('archives', ARCHIVES)

class UploadForm(FlaskForm):
    archive = FileField('Upload Dataset', validators=[
        FileRequired(),
        FileAllowed(archives, 'ZIP Files only!')
    ])
    name = StringField('Dataset Name', [validators.Required()])
    description = StringField('Description', [validators.Required()])
    submit = SubmitField('Submit')