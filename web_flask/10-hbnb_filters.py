#!/usr/bin/python3
"""
script that starts a Flask web application
"""

from flask import Flask, render_template

from models import storage

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """
    Renders the '10-hbnb_filters.html' template with the
    states and amenities data.

    Returns:
        The rendered template with the states and amenities data.
    """
    states = storage.all("State").values()
    amenities = storage.all("Amenity").values()
    print(states)
    print(amenities)

    return render_template("10-hbnb_filters.html", states=states, amenities=amenities)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
