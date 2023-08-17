from flask import Flask, jsonify, request
from main import fetch_books, format_and_print_books
from input import format_category_for_search

# from draft_config import MY_API_KEY -- not sure how essential this is, keeping in for now. Shall I push my key?

app = Flask(__name__)


@app.route("/") # Homepage route to display all the html coded on home.html file
def home():
    with open("home.html", "r") as file:
        return file.read()


@app.route("/results", methods=["POST"]) # Results page route to display output,
# Think we will also need a "GET" method attached to this route for displaying the html coded for this page.
def process_user_input():

    # Using the flask.request method to pull the user input from the html form
    selected_category = format_category_for_search(request.form["categories"]) # See input.py for category formatting
    selected_book_length = request.form["book_length"]
    # Convert dates to integers
    selected_min_published_date = int(request.form["year_published_min"])
    selected_max_published_date = int(request.form["year_published_max"])
    selected_order_by = request.form["order_by"]

    # You can now use the 'selected_' values in your Python code
    # This is just for internal purposes/testing to see what has come through as user input criteria in the console
    print(
        f"""
    Category: {selected_category}
    Book Length: {selected_book_length}
    Published Between: {selected_min_published_date} - {selected_max_published_date}
    Order By: {selected_order_by}
"""
    )

    # Declaring books variable to contain output from api search. Is this duplicate code?
    books = fetch_books(
        selected_category,
        selected_book_length,
        selected_min_published_date,
        selected_max_published_date,
        selected_order_by,
    )

    # Leaving this here in case it works with dictionary instead of class but might be redundant.
    # results = format_and_print_books(books)

    return jsonify(books)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
