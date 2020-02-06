"""
This is a simple cheatsheet webapp.
"""
import os

from flask import Flask, send_from_directory, render_template
from flask_sslify import SSLify

DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.join(DIR, 'docs', '_build', 'html')

app = Flask(__name__, template_folder=ROOT)
if 'DYNO' in os.environ:
    sslify = SSLify(app, permanent=True)

@app.errorhandler(404)
def page_not_found(e):
    """Redirect to 404.html."""
    return render_template("404.html"), 404

@app.route('/<path:path>')
def static_proxy(path):
    """Static files proxy"""
    return send_from_directory(ROOT, path)

@app.route('/')
def index_redirection():
    """Redirecting index file"""
    return send_from_directory(ROOT, 'index.html')

if __name__ == "__main__":
    app.run(debug=False)
