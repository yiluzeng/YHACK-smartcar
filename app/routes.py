import smartcar
import requests
from flask import Flask, request, jsonify, redirect, render_template, url_for
from app import app

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys

from app.firedata import db

cars_ref = db.collection(u'cars')

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return redirect('/landing')
#   return render_template('index/index.html')

@app.route('/car_info/<uid>', methods=['GET'])
def car_info(uid):
    car = cars_ref.document(uid).get()
    data = car.to_dict()
    if data is None:
        return redirect('/landing')
    else:
        data['name'] = car.get('car_make').get().get('make')
        data['features'] = car.get('car_make').get().get('features')
        data['image'] = car.get('car_make').get().get('image')

        return render_template('car_info/car_info.html', car=data);

@app.route('/car_list', methods=['GET'])
def car_list():
    cars = cars_ref.get()
    posts = []
    for car in cars:
        data = car.to_dict()
        data['name'] = car.get('car_make').get().get('make')
        data['image'] = car.get('car_make').get().get('image')
        data['uid'] = car.id

        posts.append(data)
    return render_template('car_list/car_list.html', posts=posts)


@app.route('/control_panel/client', methods=['GET'])
def control_panel_client():
    return render_template('control_panel/client-control.html')

@app.route('/control_panel/client2', methods=['GET'])
def control_panel_client2():
    return render_template('control_panel/client-control2.html')

@app.route('/control_panel/owner', methods=['GET'])
def control_panel_owner():
    return render_template('control_panel/owner-control.html')

@app.route('/control_panel/owner2', methods=['GET'])
def control_panel_owner2():
    return render_template('control_panel/owner-control2.html')


@app.route('/message', methods=['GET'])
def message():
    doc_ref = db.collection(u'requests').document(u'new')

    hide = '1'
    try:
        hide = doc_ref.get('seller').get('seller')
    except:
        hide = '1'
    return render_template('message/message.html', request=hide)

@app.route('/pending', methods=['GET'])
def pending():
    doc_ref = db.collection(u'requests').document(u'new')

    hide = '1'
    try:
        hide = doc_ref.get('seller').get('seller')
    except:
        hide = '1'
    return render_template('message/pending.html', request=hide)


@app.route('/landing', methods=['GET'])
def landing():
    return render_template('landing/landing.html')

@app.route('/make_request')
def make_request():
    data = {
        u'seller': u'zack',
        u'user': u'stanley'
    }

    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection(u'requests').document(u'new').set(data)
    return redirect(url_for('pending'))

@app.route('/delete_request')
def delete_request():
    data_ref = db.collection(u'requests').document(u'new').delete()

    return redirect(url_for('message'))

CLIENT_ID = 'cdf41817-f479-42c9-8f48-6fa2c0ff058d'
CLIENT_SECRET = 'f8ab46a3-4ec4-4172-a29a-594240fe4945'

client = smartcar.AuthClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri='http://localhost:5000/callback',
    scope=['read_vehicle_info', 'read_location', 'control_security', 'read_odometer', 'control_security', 'control_security:unlock', 'control_security:lock']
)

#hard-coded car
access_token='737ceae9-bc33-4bb4-9ff1-bb4c91319c70'

@app.route('/car_form', methods=['GET'])
def car_form():
    auth_url = client.get_auth_url(force=True)+"&mode=test"
    return render_template('car_form/car_form.html',
                           lat='41.3137799', lng='-72.9331142', url=auth_url)

@app.route('/car_auth', methods=['GET'])
def car_auth():
    auth_url = client.get_auth_url(force=True)+"&mode=test"
    return '''
<h1>Authenticate Car</h1>
<a href=%s>
<button>Connect Car</button>
</a>
''' % auth_url

@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    access = client.exchange_code(code)

    # Respond with a success status to browser
    access_token = access['access_token']
    return redirect(url_for('message'))

def get_vehicle(access_token):
    response = smartcar.get_vehicle_ids(access_token)
    vid = response['vehicles'][0]

    vehicle = smartcar.Vehicle(vid, access_token)

    return vehicle


@app.route('/get_info')
def get_info():
    vehicle = get_vehicle(access_token)
    info = vehicle.info()

    return jsonify(info)

@app.route('/get_location')
def get_location():
    vehicle = get_vehicle(access_token)
    location = vehicle.location()

    return jsonify(location)

@app.route('/get_odometer')
def get_odometer():
    vehicle = get_vehicle(access_token)
    odometer = vehicle.odometer()

    return jsonify(odometer)

@app.route('/lock_car')
def lock_car():
    vehicle = get_vehicle(access_token)

    try:
        vehicle.lock()
    except:
        return 'error'
    else:
        return 'success'

@app.route('/unlock_car')
def unlock_car():
    vehicle = get_vehicle(access_token)

    try:
        vehicle.unlock()
    except:
        return 'error'
    else:
        return 'success'
