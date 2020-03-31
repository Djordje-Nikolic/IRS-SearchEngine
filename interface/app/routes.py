from flask import render_template, redirect
from app import app
from app.forms import QueryForm

import sys
import os

if os.path.abspath("..") not in sys.path:
    sys.path.append(os.path.abspath(".."))

from sri import searchengine

engineconfigpath = "C:\\Users\\djord\\source\\repos\\IRS-SearchEngine\\sri\\config.txt"
engine = searchengine.SearchEngine(engineconfigpath)

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    form = QueryForm()
    if form.validate_on_submit():
        # form validate
        
        similarities = engine.search(form.query.data, returnobjects=True)
        similarities.sort()

        if form.maxdocs.data is not None:
            dispcount = min(form.maxdocs.data, len(similarities.list))
        else:
            dispcount = len(similarities.list)

        return render_template("main.html", title="SRI Search Engine", hellomsg="Welcome, enter your query:", form=form, results=similarities, resultcount=dispcount)
    return render_template("main.html", title="SRI Search Engine", hellomsg="Welcome, enter your query:", form=form)
