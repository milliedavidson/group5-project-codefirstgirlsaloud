from book import Book
from api import call_api_endpoint
from filters import (
    is_excluded_category,
    rating_too_low,
    get_published_year,
    book_in_date_range,
    get_book_length,
    book_matches_length,
)
from config import (
    user_input_subject,
    desired_book_length,
    start_year_input,
    end_year_input,
    order_by_input,
)


# Function to fetch books based on user input and criteria
def fetch_books(subject, book_length, start_year, end_year, order_by, min_results=10):
    results = []  # Initialise list to store results
    seen_books = set()  # Maintain a set of seen titles and authors so no repeats
    page = 1  # Starts search on page 1

    while (
        len(results) < min_results
    ):  # Keep the search going until 10 books are found (pagination)
        items = call_api_endpoint(subject, page, order_by)  # Fetch books from API

        for item in items:
            try:
                # Create book instance
                book = Book(item)

                #
                book_id = book.get_book_id
                book.length = get_book_length(book)
                published_year = get_published_year(book)

                # Check for duplicates
                if book_id in seen_books:
                    continue  # Skips over this book, as already been seen
                seen_books.add(book_id)  # If not already seen, adds it to the list

                # Check categories and rating
                if is_excluded_category(book) or rating_too_low(book):
                    continue

                # Check date range and book length
                if book_in_date_range(
                    published_year, start_year, end_year
                ) and book_matches_length(book, book_length):
                    results.append(book)  # Add book to results

            except KeyError:
                pass

        page += 1  # Moves to the next page

    return results[:min_results]  # Returns 10 results (index 0-9)


# Function to format and print book results
def format_and_print_books(book_results):
    for book in book_results:
        print(book)


# Calls the API endpoint function to fetch books
books = fetch_books(
    user_input_subject,
    desired_book_length,
    start_year_input,
    end_year_input,
    order_by_input,
)

# Format and print results
format_and_print_books(books)