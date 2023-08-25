from flask import render_template, request
from application import app
from db.functions import (
    find_books,
    format_category_for_search
)


# Homepage
# GET method provides the form for user input, POST takes these results and moves to the results page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        selected_genre = request.form.get("selected_genre")
        selected_category = request.form.get("categories")
        formatted_category = format_category_for_search(selected_category, selected_genre)
        selected_book_length = request.form["book_length"]
        selected_order_by = request.form["order_by"]

        books = find_books(
            selected_genre,
            formatted_category,
            selected_book_length,
            selected_order_by
        )

        return render_template('results.html', books=books)
    else:
        return render_template('home.html')


# Routes to 404 page
@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404
