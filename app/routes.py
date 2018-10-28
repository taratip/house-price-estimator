from app import app
from flask import render_template, url_for, redirect, flash, request, session
import ast

from app.forms import HouseForm
from app.helpers import getPropertyType
from app.predict import predict
from app.cluster import cluster


@app.route('/')
def landing():
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
                    'property_type': property_type,
                    'neighborhood': neighborhood}

        return redirect(url_for('estimate', features=features))

    return render_template('index.html', page='home', form=form)


@app.route('/estimate/<features>', methods=['GET', 'POST'])
def estimate(features):
    features_dict = ast.literal_eval(features)

    estimated_price = predict(features_dict)
    feature_houses = cluster(features_dict)

    neighborhood = features_dict['property_type']
    features_dict['property_type'] = getPropertyType(neighborhood)

    return render_template('result.html', page='result', features=features_dict, estimated_price=estimated_price, feature_houses=feature_houses)
