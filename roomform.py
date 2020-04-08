from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class RoomForm(FlaskForm):
    room = SelectField(u'Room', coerce=int, validators=[DataRequired()])
    onoff = BooleanField('Turn on light?')
    intensity = StringField('Intensity\n1-254', validators=[DataRequired()])
    submit = SubmitField('Submit')
