from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm (FlaskForm):
    searchTerm = StringField('Search Term')
    submit = SubmitField('Submit')