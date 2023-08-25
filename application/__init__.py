from flask import Flask
from db.functions import (
    format_book_published,
    format_book_rating,
    format_book_length,
)


# App creation and configuration
app = Flask(__name__)

from application import routes
# This import is intentionally below the instantiation of the Flask application

# Adding template globals
app.add_template_global(format_book_published, 'format_book_published')
app.add_template_global(format_book_rating, 'format_book_rating')
app.add_template_global(format_book_length, 'format_book_length')

