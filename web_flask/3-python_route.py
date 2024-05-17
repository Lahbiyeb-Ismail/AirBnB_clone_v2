#!/usr/bin/python3

"""
script that starts a Flask web application
"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """
    This function returns a greeting message.
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    Returns the string "HBNB".
    """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """
    Replaces underscores in the given text with spaces
    and prefixes the text with 'C'.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with underscores replaced
        by spaces and prefixed with 'C'.
    """
    new_text = [" "] * len(text)

    for i in range(len(text)):
        if text[i] != "_":
            new_text[i] = text[i]
        else:
            new_text[i] = " "

    new_text = "".join(new_text)

    return f"C {new_text}"


@app.route("/python/", defaults={"text": "is cool"}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text):
    """
    Replaces underscores with spaces in the given text
    and returns a formatted string.

    Args:
        text (str): The input text to be processed.

    Returns:
        str: A formatted string with "Python" followed
        by the modified text.

    Example:
        >>> python_route("hello_world")
        'Python hello world'
    """
    new_text = text.replace("_", " ")
    return f"Python {new_text}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
