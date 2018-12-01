import smartcar
import requests
from flask import Flask, request, jsonify, redirect, render_template
from app import app

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index/index.html')

@app.route('/car_info', methods=['GET'])
def car_info():
    return render_template('car_info/car_info.html')

@app.route('/car_list', methods=['GET'])
def car_list():
    return render_template('car_list/car_list.html')

@app.route('/car_form', methods=['GET'])
def car_form():
    return render_template('car_form/car_form.html')

@app.route('/control_panel', methods=['GET'])
def control_panel():
    return render_template('control_panel/control_panel.html')

@app.route('/car_status', methods=['GET'])
def car_status():
    return render_template('car_status/car_status.html')

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

