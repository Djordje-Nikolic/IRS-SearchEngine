from flask import render_template, redirect, jsonify, request
from app import app
from app.forms import QueryForm

import sys
import os

if os.path.abspath("..") not in sys.path:
    sys.path.append(os.path.abspath(".."))

from sri import searchengine

engine = searchengine.SearchEngine(os.path.abspath(app.config['ENGINE_CONFIG']))

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    form = QueryForm()
    return render_template("main.html", title="SRI Search Engine", hellomsg="", form=form)

@app.route('/search', methods=['GET','POST'])
def search():
    form = QueryForm(request.args)
    if form.validate():
        # form validate
        
        similarities = engine.search(form.query.data, returnobjects=True, prf=form.prf.data)
        similarities.sort()

        pagesize = int(form.pagesize.data)
        currentPage = request.args.get('page')
        if currentPage is None:
            currentPage = 0

        offset = int(currentPage) * pagesize
        
        return jsonify(data=similarities.serialize(fullfilepath=form.fullpath.data, offset=offset, count=pagesize))
    else:
        errorList = []
        for field, errors in form.errors.items():
            errorList.append("Field: {0} Errors: {1}".format(form[field].label, ', '.join(errors)))
        return jsonify(data=None, errors=errorList)

@app.route('/open', methods=['GET'])
def openfile():
    fileid = request.args.get('fileid')
    
    if fileid is not None:
        fileid = int(fileid)
    
    filecontent = engine.getFileContent(fileid)
    
    if filecontent is not None:
        return filecontent