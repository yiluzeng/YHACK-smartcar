import smartcar
from flask import Flask, request, jsonify
from app import app

CLIENT_ID = 'cdf41817-f479-42c9-8f48-6fa2c0ff058d'
CLIENT_SECRET = 'f8ab46a3-4ec4-4172-a29a-594240fe4945'

client = smartcar.AuthClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri='http://localhost:5000/callback',
    scope=['read_vehicle_info', 'read_location', 'control_security']
    )

@app.route('/car_auth', methods=['GET'])
def carAuth():
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

