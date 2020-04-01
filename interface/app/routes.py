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
@app.route('/test', methods=['GET','POST'])
def home():
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
    return render_template("main.html", title="SRI Search Engine", hellomsg="Welcome, enter your query", form=form)
