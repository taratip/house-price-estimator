import pandas as pd
import numpy as np
import os
import urllib
import requests
import xml.etree.ElementTree as ET

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy import stats
from scipy.spatial.distance import cdist

from app import app


def cluster(data):
    # Get path of app directory
    path = os.path.abspath(os.path.dirname(__file__)) + '/data/'
    cluster_csv_name = 'cluster_df.csv'
    all_csv_name = 'all_types.csv'

    cluster_csv_path = path + cluster_csv_name
    all_csv_path = path + all_csv_name

    all_df = pd.read_csv(all_csv_path)
    df = pd.read_csv(cluster_csv_path)
    df = df.drop(['Unnamed: 0'], axis=1)

    scale = StandardScaler()
    df_std = scale.fit_transform(X)

    kmeans = KMeans(n_clusters=50)
    kmeans = kmeans.fit(df_std)
    labels = kmeans.predict(df_std)

    # Create user input features
    user_input = {
        'bedrooms': int(data['bedroom']),
        'bathrooms': float(data['bathroom']),
        'finished_SqFt': float(data['finished_sq_ft']),
        'total_rooms': float(data['total_room']),
        'Allston': 1 if data['neighborhood'] == 'Allston' else 0,
        'Back Bay': 1 if data['neighborhood'] == 'Back Bay' else 0,
        'Bay Village': 1 if data['neighborhood'] == 'Bay Village' else 0,
        'Beacon Hill': 1 if data['neighborhood'] == 'Beacon Hill' else 0,
        'Brighton': 1 if data['neighborhood'] == 'Brighton' else 0,
        'Charlestown': 1 if data['neighborhood'] == 'Charlestown' else 0,
        'Chinatown': 1 if data['neighborhood'] == 'Chinatown' else 0,
        'Downtown': 1 if data['neighborhood'] == 'Downtown' else 0,
        'Downtown Crossing': 1 if data['neighborhood'] == 'Downtown Crossing' else 0,
        'East Boston': 1 if data['neighborhood'] == 'East Boston' else 0,
        'Fenway': 1 if data['neighborhood'] == 'Fenway' else 0,
        'Hyde Park': 1 if data['neighborhood'] == 'Hyde Park' else 0,
        'Jamaica Plain': 1 if data['neighborhood'] == 'Jamaica Plain' else 0,
        'Kenmore': 1 if data['neighborhood'] == 'Kenmore' else 0,
        'Leather District': 1 if data['neighborhood'] == 'Leather District' else 0,
        'Mattapan': 1 if data['neighborhood'] == 'Mattapan' else 0,
        'Mission Hill': 1 if data['neighborhood'] == 'Mission Hill' else 0,
        'North Dorchester': 1 if data['neighborhood'] == 'North Dorchester' else 0,
        'North End': 1 if data['neighborhood'] == 'North End' else 0,
        'Roslindale': 1 if data['neighborhood'] == 'Roslindale' else 0,
        'Roxbury': 1 if data['neighborhood'] == 'Roxbury' else 0,
        'South Boston': 1 if data['neighborhood'] == 'South Boston' else 0,
        'South Dorchester': 1 if data['neighborhood'] == 'South Dorchester' else 0,
        'South End': 1 if data['neighborhood'] == 'South End' else 0,
        'West End': 1 if data['neighborhood'] == 'West End' else 0,
        'West Roxbury': 1 if data['neighborhood'] == 'West Roxbury' else 0,
        'Winthrop': 1 if data['neighborhood'] == 'Winthrop' else 0}

    user_df = pd.DataFrame(user_input, index=[0])

    # Get cluster for user input
    user_cluster = kmeans.predict(user_df)
    # Get distance from user input datapoint
    trans = kmeans.transform(df_std)
    # Sort distance
    closest_points = []
    for i, argsortidx in enumerate(argsor):
        if i == 3:
            break
        closest_points.append(argsortidx)

    zpids = []
    addresses = []
    prices = []
    sold_dates = []

    # Get index of the 3 shortest distance from user cluster
    for i in closest_points:
        zpid = all_df.loc[i, 'zpid']
        zpids.append(zpid)

        add = all_df.loc[i, 'address']
        addresses.append(add)

        price = 'Last sold price: ${0:.2f} M'.format(all_df.loc[i, 'price']/1000000.0)
        prices.append(price)

        sold_date = 'Sold on: {}'.format(all_df.loc[i, 'readable_date_sold'])
        sold_dates.append(sold_date)

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

    result = {
        'addresses': addresses,
        'prices': prices,
        'sold_dates': sold_dates,
        'home_urls': home_urls,
        'pic_urls': pic_urls
    }

    return result
