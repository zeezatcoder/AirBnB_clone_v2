#!/usr/bin/python3
"""starts a Flask web application
- web application should be listening on 0.0.0.0, port 5000
Routes:
        - /: display “Hello HBNB!”
- strict_slashes=False should be specified in the route
"""
from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    return("Hello HBNB!")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=None)
