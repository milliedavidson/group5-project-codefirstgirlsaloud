import random
import time
from api import call_api
from book import create_book_dict
from helper_functions import (
    get_book_id,
    excluded_categories,
    low_rating,
    get_published_year,
    book_in_date_range,
    get_book_length,
    format_and_print_books,
)
from config import (
    user_subject,
    user_book_length,
    user_start_year,
    user_end_year,
    user_order_by,
)

start_time = time.time()  # Remove later - just for testing purposes


# Function to fetch books based on user input and criteria
def find_books(subject, book_length, start_year, end_year, order_by, min_results=10):
    results = []  # Initialise list to store results
    seen_books = set()  # Maintain a set of seen titles and authors so no repeats
    page = random.randint(0, 5)  # Starts search on random page number between 0-10

    while (
        len(results) < min_results
    ):  # Keep the search/loop going until 10 books are found (pagination)
        items = call_api(subject, page, order_by)  # Fetch books from API

        for item in items:
            try:
                # Create book dictionary
                book_dict = create_book_dict(item)

                # 1st filter removes anything with missing data
                if any(value == "N/A" or value == 0 for value in book_dict.values()):
                    continue

                # 2nd filter check for duplicates to ensure unique books in the results
                book_id = get_book_id(book_dict)
                if book_id in seen_books:
                    continue  # Skips over this book, as already been seen
                seen_books.add(book_id)  # If not already seen, adds it to the list

                # 3rd filter checks if there are any excluded categories and if rating is 4+
                if excluded_categories(book_dict) or low_rating(book_dict):
                    continue

                # 4th filter checks within date range and selected book length
                year = get_published_year(book_dict)
                length = get_book_length(book_dict)
                if (
                    book_in_date_range(year, start_year, end_year)
                    and length == book_length
                ):
                    # If the book gets through these filters it is added book to results
                    results.append(book_dict)

            except KeyError:
                pass

        page += random.randint(
            1, 5
        )  # Moves to new page by adding a random number between 1-10

    return results[:min_results]  # Returns 10 results (index 0-9)


# Calls the API endpoint function to fetch books
books = find_books(
    user_subject, user_book_length, user_start_year, user_end_year, user_order_by
)

# Format and print results
format_and_print_books(books)


# Remove later - just for testing purposes
end_time = time.time()
run_time = end_time - start_time
print(run_time)
