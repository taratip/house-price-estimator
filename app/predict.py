import numpy as np
import pandas as pd
import os
import urllib
import requests
import xml.etree.ElementTree as ET

from sklearn import ensemble
from sklearn.ensemble import GradientBoostingRegressor

from app import app
from app.helpers import getGroup


def predict(data):
    # Create dictionary for input home features
    home_dict = {}
    print(data)
    cluster_group = getGroup(data['neighborhood'])

    if cluster_group == 'low_freq':
        home_dict['low_freq'] = 1
        home_dict['low_price_high_freq'] = 0
        home_dict['high_price_high_freq'] = 0
    elif cluster_group == 'low_price_high_freq':
        home_dict['low_freq'] = 0
        home_dict['low_price_high_freq'] = 1
        home_dict['high_price_high_freq'] = 0
    else:
        home_dict['low_freq'] = 0
        home_dict['low_price_high_freq'] = 0
        home_dict['high_price_high_freq'] = 1

    if data['property_type'] == 'APARTMENT':
        home_dict['APARTMENT'] = 1
        home_dict['CONDO'] = 0
        home_dict['MULTI_FAMILY'] = 0
        home_dict['SINGLE_FAMILY'] = 0
        home_dict['TOWNHOUSE'] = 0
    elif data['property_type'] == 'CONDO':
        home_dict['APARTMENT'] = 0
        home_dict['CONDO'] = 1
        home_dict['MULTI_FAMILY'] = 0
        home_dict['SINGLE_FAMILY'] = 0
        home_dict['TOWNHOUSE'] = 0
    elif data['property_type'] == 'MULTI_FAMILY':
        home_dict['APARTMENT'] = 0
        home_dict['CONDO'] = 0
        home_dict['MULTI_FAMILY'] = 1
        home_dict['SINGLE_FAMILY'] = 0
        home_dict['TOWNHOUSE'] = 0
    elif data['property_type'] == 'SINGLE_FAMILY':
        home_dict['APARTMENT'] = 0
        home_dict['CONDO'] = 0
        home_dict['MULTI_FAMILY'] = 0
        home_dict['SINGLE_FAMILY'] = 1
        home_dict['TOWNHOUSE'] = 0
    else:
        home_dict['APARTMENT'] = 0
        home_dict['CONDO'] = 0
        home_dict['MULTI_FAMILY'] = 0
        home_dict['SINGLE_FAMILY'] = 0
        home_dict['TOWNHOUSE'] = 1

    home_dict['bedrooms'] = int(data['bedroom'])
    home_dict['bathrooms'] = float(data['bathroom'])
    home_dict['total_rooms'] = float(data['total_room'])
    home_dict['lot_size'] = int(data['lot_size'])
    home_dict['bed_bath'] = home_dict['bedrooms'] / home_dict['bathrooms']
    home_dict['finished_SqFt'] = float(data['finished_sq_ft'])
    home_dict['finishedsqft_rooms'] = home_dict['finished_SqFt'] / home_dict['total_rooms']
    home_dict['age'] = 2018 - int(data['built_year'])
    home_dict['lot_finish'] = home_dict['lot_size'] / home_dict['finished_SqFt']

    # Create DataFrame for home features
    home_df = pd.DataFrame(home_dict, index=[0])

    # Get path of app directory
    path = os.path.abspath(os.path.dirname(__file__)) + '/data/'
    csv_name = 'all_types.csv'
    csv_path = path + csv_name

    # Read home data file
    df = pd.read_csv(csv_path)

    X = df[['bathrooms', 'bedrooms', 'finished_SqFt', 'total_rooms',
            'finishedsqft_rooms', 'bed_bath', 'age', 'lot_size', 'lot_finish']]

    y = df['adj_price_m']
    group = pd.get_dummies(df['group'])
    home_type = pd.get_dummies(df['home_type'])

    X = pd.concat([X, group, home_type], axis=1)

    # Run the model
    gbr = ensemble.GradientBoostingRegressor()
    model_gbr = gbr.fit(X, y)

    home_X = home_df[['bathrooms', 'bedrooms', 'finished_SqFt', 'total_rooms',
                      'finishedsqft_rooms', 'bed_bath', 'age', 'lot_size', 'lot_finish', 'high_price_high_freq', 'low_freq', 'low_price_high_freq', 'APARTMENT', 'CONDO', 'MULTI_FAMILY', 'SINGLE_FAMILY', 'TOWNHOUSE']]

    # Predict
    prediction = model_gbr.predict(home_X)

    estimation = round(prediction[0], 2)

    # Get similar features houses
    df = df[(df['finished_SqFt'] >= 0.8 * float(data['finished_sq_ft'])) &
            (df['finished_SqFt'] <= 1.2 * float(data['finished_sq_ft']))]
    # df = df[(df['bathrooms'] >= float(data['bathroom']) - 0.5) &
    #         (df['bathrooms'] <= float(data['bathroom']) + 0.5)]
    # df = df[(df['bedrooms'] >= int(data['bedroom']) - 1) &
    #         (df['bedrooms'] <= int(data['bedroom']) + 1)]
    # df = df[df['bedrooms'] == int(data['bedroom'])]
    df = df[df['neighborhood'] == data['neighborhood']]
    # df = df[df['group'] == cluster_group]
    # df = df[df['total_rooms'] == float(data['total_room'])]
    df.sort_values(by=['readable_date_sold'])

    print(df[['group', 'bathrooms', 'bedrooms', 'neighborhood', 'total_rooms', 'finished_SqFt']])

    if len(df.index) > 3:
        loop_num = 3
    else:
        loop_num = len(df.index)

    addresses = []
    prices = []
    dates = []
    zpids = []

    for i in range(loop_num):
        add = df.iloc[i, 2]
        addresses.append(add)

        price = 'Last sold price: ${} M'.format(str(df.iloc[i, 6]/1000000.0))
        prices.append(price)

        date = 'Sold on: {}'.format(df.iloc[i, 8])
        dates.append(date)

        zpid = df.iloc[i, -1]
        zpids.append(zpid)

    print(addresses)
    print(prices)
    print(dates)
    print(zpids)

    # Get picture by zpid
    pic_urls = []
    home_urls = []

    zillow_id = app.config['ZILLOW_API_KEY']
    url = 'http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?'
    tree = ''

    for id in zpids:
        zpid_data = {'zws-id': zillow_id, 'zpid': id}
        query_string = url + urllib.parse.urlencode(zpid_data)

        response = requests.get(query_string)

        msg = response.content
        tree = ET.fromstring(msg)

        code = tree.find('message/code')

        if code.text == '0':
            result = tree.find('response')

            homeInfo = result.find('links/homeInfo')
            images = result.find('images/image')

            home_url = homeInfo.text if homeInfo is not None else None
            pic_url = images[0].text if images[0] is not None else 'http://source.unsplash.com/daily'

            home_urls.append(home_url)
            pic_urls.append(pic_url)
        else:
            home_urls.append(None)
            pic_urls.append('http://source.unsplash.com/daily')

    est_price = '{} M'.format(estimation)
    result = {
        'estimation': est_price, 'home_dict': home_dict, 'addresses': addresses, 'pic_urls': pic_urls, 'home_urls': home_urls, 'prices': prices, 'dates': dates
    }

    return result
