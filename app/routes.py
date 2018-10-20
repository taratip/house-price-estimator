from app import app
from flask import render_template, url_for, redirect, flash, request
from app.forms import HouseForm


@app.route('/')
def landing():
    return render_template('landing.html', page='landing')


@app.route('/index')
def index():
    form = HouseForm()
    return render_template('index.html', page='home', form=form)


@app.route('/estimate', methods=['GET', 'POST'])
def estimate():
    features = {}
    if request.method == 'POST':
        finished_sq_ft = request.form["inputSqFt"]
        lot_size = request.form["inputLot"]
        bedroom = request.form["inputBed"]
        bathRoom = request.form["inputBath"]
        total_room = request.form["inputYear"]
        built_year = request.form["inputYear"]
        features = {'finishedSqFt': finished_sq_ft, 'lotSize': lot_size}
    return render_template('result.html', page='result', features=features)
