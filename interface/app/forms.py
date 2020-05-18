from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
    query = StringField('Query', validators=[DataRequired()])
    pagesize = IntegerField('Documents per page', default=10)
    fullpath = BooleanField('Display document path?')
    prf = BooleanField('Use pseudo-relevance feedback?', default=True)
    submit = SubmitField('Search')