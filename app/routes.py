import smartcar
import requests
from flask import Flask, request, jsonify, redirect, render_template
from app import app

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("yhack-smartcar-firebase-adminsdk-6aysw-1bf4fe0230.json")


firebase_admin.initialize_app(cred, {
'databaseURL': 'https://yhack-smartcar.firebaseio.com'
})


db = firestore.client()

cars_ref = db.collection(u'cars')

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return redirect('/landing')
#   return render_template('index/index.html')

@app.route('/car_info', methods=['GET'])
def car_info():
    return render_template('car_info/car_info.html')

@app.route('/car_list', methods=['GET'])
def car_list():
    cars = cars_ref.get()
    posts = []
    for car in cars:
        data = car.to_dict()
        data['name'] = car.get('car_make').get().get('make')
        data['image'] = car.get('car_make').get().get('image')

        posts.append(data)
    return render_template('car_list/car_list.html', posts=posts)

@app.route('/car_form', methods=['GET'])
def car_form():
    return render_template('car_form/car_form.html',
            lat='41.3137799', lng='-72.9331142')

@app.route('/control_panel/client', methods=['GET'])
def control_panel_client():
    return render_template('control_panel/client-control.html')

@app.route('/control_panel/client2', methods=['GET'])
def control_panel_client2():
    return render_template('control_panel/client-control2.html')

@app.route('/control_panel/owner', methods=['GET'])
def control_panel_owner():
    return render_template('control_panel/owner-control.html')

@app.route('/car_status', methods=['GET'])
def car_status():
    return render_template('car_status/car_status.html')

@app.route('/landing', methods=['GET'])
def landing():
    return render_template('landing/landing.html')

CLIENT_ID = 'cdf41817-f479-42c9-8f48-6fa2c0ff058d'
CLIENT_SECRET = 'f8ab46a3-4ec4-4172-a29a-594240fe4945'

client = smartcar.AuthClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri='http://localhost:5000/callback',
    scope=['read_vehicle_info', 'read_location', 'control_security', 'read_odometer', 'control_security', 'control_security:unlock', 'control_security:lock']
)

#hard-coded car
access_token='0f3ecfb0-fd28-497c-ac13-22605ea94d08'

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

    # Log the access token response
    print(access)

    # Respond with a success status to browser
    return jsonify(access)

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
