from flask import Flask, jsonify, request
from main import fetch_books, format_and_print_books
from input import format_category_for_search

# from draft_config import MY_API_KEY

app = Flask(__name__)


@app.route("/")
def home():
    with open("home.html", "r") as file:
        return file.read()


@app.route("/results", methods=["POST"])
def process_user_input():
    # selected_genre = request.form['genres'] -- Not sure if this is needed at all, though keeping here with regards
    # to Olivia's comment about excluding fiction from non-fiction searches

    selected_category = format_category_for_search(request.form["categories"])
    selected_book_length = request.form["book_length"]
    selected_min_published_date = int(request.form["year_published_min"])
    selected_max_published_date = int(request.form["year_published_max"])
    selected_order_by = request.form["order_by"]

    # You can now use the 'selected_' values in your Python code
    # This is just for internal purposes to see what has come through as user input criteria
    print(
        f"""
    Category: {selected_category}
    Book Length: {selected_book_length}
    Published Between: {selected_min_published_date} - {selected_max_published_date}
    Order By: {selected_order_by}
"""
    )

    books = fetch_books(
        selected_category,
        selected_book_length,
        selected_min_published_date,
        selected_max_published_date,
        selected_order_by,
    )

    # results = format_and_print_books(books)

    return jsonify(books)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
