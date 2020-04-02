from flask import render_template, redirect, jsonify
from app import app
from app.forms import QueryForm

import sys
import os

if os.path.abspath("..") not in sys.path:
    sys.path.append(os.path.abspath(".."))

from sri import searchengine

engine = searchengine.SearchEngine(app.config['ENGINE_CONFIG'])

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    form = QueryForm()
    return render_template("main.html", title="SRI Search Engine", hellomsg="Welcome, enter your query", form=form)

@app.route('/search', methods=['GET','POST'])
def search():
    form = QueryForm()
    if form.validate_on_submit():
        # form validate
        
        similarities = engine.search(form.query.data, returnobjects=True)
        similarities.sort()

        if form.maxdocs.data != 0:
            dispcount = min(form.maxdocs.data, len(similarities.list))
        else:
            dispcount = len(similarities.list)
        
        return jsonify(data=similarities.serialize(), dispcount=dispcount)
    else:
        errorList = []
        for field, errors in form.errors.items():
            errorList.append("Field: {0} Errors: {1}".format(form[field].label, ', '.join(errors)))
        return jsonify(data=None, errors=errorList)
