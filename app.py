from flask import Flask
from flask import request
from flask import render_template
import json
from src.functions import extraction
app = Flask("__name__")

@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    # environ.headers['Access-Control-Allow-Method']='*'
    # environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ

dic = {}

@app.route('/adm_user/query_r/', methods=['POST'])
def query():
    url = request.form["url"]
    global dic
    dic = extraction(url)
    return render_template('show.html')
@app.route('/shuju/')
def query2():
    return dic

if __name__ == '__main__':
    app.run()

