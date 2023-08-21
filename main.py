from flask import Flask, render_template, request
from functions import (
    find_books,
    format_book_published,
    format_book_categories,
    format_book_rating,
    format_book_length, format_category_for_search,
    # format_category_for_search
)

app = Flask(__name__, template_folder='templates')
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
        selected_order_by = request.form["order_by"]

        # Delete later on - just prints to console
        print(f"Selected Genre: {selected_genre}")
        print(f"Selected Category: {selected_category}")
        print(f"Selected Book Length: {selected_book_length}")
        print(f"Selected Min Published Date: {selected_min_published_date}")
        print(f"Selected Max Published Date: {selected_max_published_date}")
        print(f"Selected Order By: {selected_order_by}")

        books = find_books(
            formatted_category,
            selected_book_length,
            selected_min_published_date,
            selected_max_published_date,
            selected_order_by
        )
        return render_template('results.html', books=books)
    else:
        return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)

