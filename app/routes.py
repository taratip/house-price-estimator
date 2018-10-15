from app import app
from flask import render_template, url_for


@app.route('/')
def landing():
    return render_template('landing.html', page='landing')


@app.route('/index')
def index():
    return render_template('index.html', page='home')
