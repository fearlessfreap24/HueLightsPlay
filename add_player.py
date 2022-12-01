from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import NumberRange, DataRequired, Length
from flask_wtf import FlaskForm

class Add_Player(FlaskForm):
    index = IntegerField("Index")
    name = StringField("Player's Name", validators=[DataRequired()])
    ign = StringField("In Game Name", validators=[DataRequired()])
    location = StringField("Player's Location")
    b_mo = IntegerField("Birth Month", validators=[NumberRange(1,12)])
    b_day = IntegerField("Birthday Day of Month", validators=[NumberRange(1,31)])