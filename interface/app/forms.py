from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
    query = StringField('Query', validators=[DataRequired()])
    maxdocs = IntegerField('Number of documents to return')
    fullpath = BooleanField('Display document path?')
    submit = SubmitField('Search')