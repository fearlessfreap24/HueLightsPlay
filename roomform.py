from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    room = StringField('Username', validators=[DataRequired()])
    onoff = BooleanField('On/Off')
    intensity = StringField('Intensity')
    submit = SubmitField('Submit')
