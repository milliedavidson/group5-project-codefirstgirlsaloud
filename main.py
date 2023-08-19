from flask import Flask, render_template
from functions import (
    find_books,
    # format_and_print_books,
    format_book_published,
    format_book_categories,
    format_book_rating,
    format_book_length
)
from config import (
    user_subject,
    user_book_length,
    user_start_year,
    user_end_year,
    user_order_by
)

app = Flask(__name__, template_folder='templates')
app.add_template_global(format_book_published, 'format_book_published')
app.add_template_global(format_book_categories, 'format_book_categories')
app.add_template_global(format_book_rating, 'format_book_rating')
app.add_template_global(format_book_length, 'format_book_length')


# Calls the API endpoint function to fetch books
books = find_books(
    user_subject, user_book_length, user_start_year, user_end_year, user_order_by
)


@app.route('/')
def book_search_results():
    # Calls the API endpoint function to fetch books
    books = find_books(
        user_subject, user_book_length, user_start_year, user_end_year, user_order_by
    )

    return render_template('results.html', books=books)


if __name__ == '__main__':
    app.run()
