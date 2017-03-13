#!/usr/bin/env python3.5
from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!<h2>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!<h2>' % name


if __name__ == '__main__':
    app.run(debug=True)
