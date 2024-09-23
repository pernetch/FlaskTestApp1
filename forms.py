from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#simple formulaire
class NameForm(FlaskForm):
    name = StringField('Indiquez votre nom',validators=[DataRequired()])
    submit = SubmitField('Submit')