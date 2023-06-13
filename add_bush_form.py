from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import NumberRange, DataRequired, Length
from flask_wtf import FlaskForm

class Add_Bush(FlaskForm):
    bush_type = SelectField(
        "Bush Type",
        choices=["Spear Grass",
        "Marmalade Bush",
        "Golden Bell",
        "Purple Smokebush",
        "Butterfly Bush"]
        )
    sender = StringField("Sender", validators=[DataRequired(), Length(min=3, max=25)])
    diamonds = IntegerField("Diamonds",validators=[NumberRange(0,20), DataRequired()])
    ribbons = IntegerField("Ribbons",validators=[NumberRange(0,100)])

