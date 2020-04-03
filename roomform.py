from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    room = StringField('Room', validators=[DataRequired()])
    onoff = BooleanField('On/Off')
    intensity = StringField('Intensity\n1-256')
    submit = SubmitField('Submit')
