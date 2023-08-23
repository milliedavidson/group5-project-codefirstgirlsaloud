from flask import render_template, request
from application import app
from db.functions import (
    find_books,
    format_book_published,
    format_book_categories,
    format_book_rating,
    format_book_length,
    format_category_for_search
)


app.add_template_global(format_book_published, 'format_book_published')
app.add_template_global(format_book_categories, 'format_book_categories')
app.add_template_global(format_book_rating, 'format_book_rating')
app.add_template_global(format_book_length, 'format_book_length')


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        selected_genre = request.form.get("selected_genre")
        selected_category = request.form.get("categories")
        formatted_category = format_category_for_search(selected_category, selected_genre)
        selected_book_length = request.form["book_length"]
        selected_min_published_date = int(request.form["year_published_min"])
        selected_max_published_date = int(request.form["year_published_max"])

        # Delete later on - just prints to console
        print(f"Selected Genre: {selected_genre}")
        print(f"Selected Category: {selected_category}")
        print(f"Selected Book Length: {selected_book_length}")
        print(f"Selected Min Published Date: {selected_min_published_date}")
        print(f"Selected Max Published Date: {selected_max_published_date}")

        books = find_books(
            formatted_category,
            selected_book_length,
            selected_min_published_date,
            selected_max_published_date,

        )
        return render_template('results.html', books=books)
    else:
        return render_template('home.html')


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404
