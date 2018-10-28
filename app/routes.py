from app import app
from flask import render_template, url_for, redirect, flash, request, session
from app.forms import HouseForm
from app.helpers import getPropertyType
from app.predict import predict


@app.route('/')
def landing():
    # if session.get('features') == True:
    #     session.pop('features', None)

    return render_template('landing.html', page='landing')


@app.route('/index', methods=['GET', 'POST'])
def index():
    # if session.get('features') == True:
    #     session.pop('features', None)

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

        # session['features'] = features

        return redirect(url_for('estimate', features=features))

    return render_template('index.html', page='home', form=form)


@app.route('/estimate/<features>', methods=['GET', 'POST'])
def estimate():
    # features = session.get('features')
    result = predict(features)

    neighborhood = features['property_type']
    features['property_type'] = getPropertyType(neighborhood)

    # result = {
    #     'estimation': '4.29 M', 'home_dict': {'low_freq': 1, 'low_price_high_freq': 0, 'high_price_high_freq': 0, 'APARTMENT': 0, 'CONDO': 1, 'MULTI_FAMILY': 0, 'SINGLE_FAMILY': 0, 'TOWNHOUSE': 0, 'bedrooms': 2, 'bathrooms': 1.0, 'total_rooms': 4.0, 'lot_size': 3904, 'bed_bath': 2.0, 'finished_SqFt': 3624.0, 'finishedsqft_rooms': 906.0, 'age': 17, 'lot_finish': 1.0772626931567328}, 'addresses': ['20 Isabella St'], 'pic_urls': ['https://photos.zillowstatic.com/p_d/ISpll0ou4ehr0m0000000000.jpg'], 'home_urls': ['https://www.zillow.com/homedetails/20-Isabella-St-Boston-MA-02116/2121181784_zpid/'], 'prices': ['Last sold price: $2.4 M'], 'dates': ['Sold on: 2016-07-07']}
    return render_template('result.html', page='result', features=features, result=result)
