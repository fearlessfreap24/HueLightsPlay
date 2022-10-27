from wtforms import StringField, DateField, IntegerField, SubmitField
from wtforms.validators import NumberRange, DataRequired, Length
from flask_wtf import FlaskForm

class Add_Bush(FlaskForm):
    bush_type = StringField("Bush Type", validators=[DataRequired(), Length(min=3, max=25)])
    date = DateField("Date", validators=[DataRequired()])
    sender = StringField("Sender", validators=[DataRequired(), Length(min=3, max=25)])
    diamonds = IntegerField("Diamonds",validators=[NumberRange(0,20)])
    ribbons = IntegerField("Ribbons",validators=[NumberRange(0,100)])


