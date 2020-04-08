from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class RoomForm(FlaskForm):
    room = SelectField(u'Room')
    onoff = BooleanField('On/Off')
    intensity = StringField('Intensity\n1-256')
    submit = SubmitField('Submit')
