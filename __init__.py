from flask import Flask

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

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
