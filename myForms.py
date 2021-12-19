from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField

class SearchForm(FlaskForm):
    term=StringField(label='Search Term')
    num=IntegerField(label='Number of Tweets')
    submit=SubmitField(label='Submit')
