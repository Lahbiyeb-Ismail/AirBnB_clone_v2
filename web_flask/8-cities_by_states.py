#!/usr/bin/python3
"""
script that starts a Flask web application
"""

from flask import Flask, render_template

from models import storage

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """
    Retrieve a list of states and render them in a template.

    Returns:
        The rendered template with the list of states.
    """
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)

    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
