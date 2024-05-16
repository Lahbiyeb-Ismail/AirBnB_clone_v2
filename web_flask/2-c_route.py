"""
script that starts a Flask web application
"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    return "Hello, HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    new_text = [" "] * len(text)

    # new_text = text.replace("_", " ")
    for i in range(len(text)):
        if text[i] != "_":
            new_text[i] = text[i]
        else:
            new_text[i] = " "

    new_text = "".join(new_text)

    return f"C {new_text}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
