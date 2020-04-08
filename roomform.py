from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class RoomForm(FlaskForm):
    room = SelectField(u'Room', coerce=int, validators=[DataRequired()])
    onoff = BooleanField('On/Off')
    intensity = StringField('Intensity\n1-256', validators=[DataRequired()])
    submit = SubmitField('Submit')
