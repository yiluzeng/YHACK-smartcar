@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


@app.route('/home', methods=['GET'])
def home():
    return render_template('home/home.html')


@app.route('/car-info', methods=['GET'])
def car-info():
    return render_template('car-info/car-info.html')

@app.route('/car-form', methods=['GET'])
def
