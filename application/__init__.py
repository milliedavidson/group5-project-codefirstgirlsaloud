from flask import Flask

app = Flask(__name__)

from application import routes
# This import is intentionally below the instantiation of the Flask application
