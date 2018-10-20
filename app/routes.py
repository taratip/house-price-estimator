from app import app
from flask import render_template, url_for, redirect, flash, request, session
from app.forms import HouseForm
from app.helpers import getPropertyType


@app.route('/')
def landing():
    session.pop('features', None)
    return render_template('landing.html', page='landing')


@app.route('/index', methods=['GET', 'POST'])
def index():
    features = {}
    form = HouseForm(request.form)

    if form.validate_on_submit():
        finished_sq_ft = form.finished_sq_ft.data
        lot_size = form.lot_size.data
        bedroom = form.bedroom.data
        bathroom = form.bathroom.data
        total_room = form.total_room.data
        built_year = form.built_year.data
        property_type = form.property_type.data
        neighborhood = form.neighborhood.data

        features = {'finished_sq_ft': finished_sq_ft,
                    'lot_size': lot_size,
                    'bedroom': bedroom,
                    'bathroom': bathroom,
                    'total_room': total_room,
                    'built_year': built_year,
                    'property_type': getPropertyType(property_type),
                    'neighborhood': neighborhood}

        session['features'] = features

        return redirect(url_for('estimate'))

    return render_template('index.html', page='home', form=form)


@app.route('/estimate', methods=['GET', 'POST'])
def estimate():
    features = session.get('features')

    return render_template('result.html', page='result', features=features)
