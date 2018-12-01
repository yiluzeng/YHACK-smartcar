# YHACK-smartcar
smart car rental service

To run flask app, first create a virtual environment
```
$ python3 -m venv venv
```
Then activate it
```
$ source venv/bin/activate
```

Install requirements with
```
$ pip install -r requirements.txt
```

Set environment variables
```
$ export FLASK_APP=run.py
```

It also helps to go into debugging mode for development, so the server automatically restarts when a file is changed
```
$ export DEBUG=1
```

To run the server:
```
$ flask run
```

Then visit http://localhost:5000/
