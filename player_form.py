from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import NumberRange, DataRequired, Length
from flask_wtf import FlaskForm

class Player_Form(FlaskForm):
    id = IntegerField(
        "ID",
        validators=[
            NumberRange(1,15)
            ,DataRequired()
        ])
    name = StringField(
        "Player's Name",
        validators=[
            DataRequired(),
            Length(max=30)
        ])
    ign = StringField(
        "In Game Name",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )
    location = StringField(
        "Player's Location",
        validators=[
            Length(max=30)
        ]
    )
    b_mo = IntegerField(
        "Birth Month",
        validators=[
            NumberRange(min=1, max=12)
        ]
    )
    b_day = IntegerField(
        "Birth Date",
        validators=[
            NumberRange(min=1, max=31)
        ]
    )
    