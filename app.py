from flask import Flask
from flask import request
from flask import render_template
import json
from src.functions import extraction, data_match

app = Flask(__name__)


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    # environ.headers['Access-Control-Allow-Method']='*'
    # environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ


personal_data = {}


@app.route('/home')
def render_home():
    return render_template('home.html')


@app.route('/query', methods=['POST'])
def query():
    url = request.form["url"]
    global personal_data
    personal_data = extraction(url)
    personal_data = data_match(personal_data)
    return render_template('show.html')


@app.route('/data')
def get_data():
    return personal_data


def main():
    app.run()


if __name__ == '__main__':
    main()
