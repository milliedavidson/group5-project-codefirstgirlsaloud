from datetime import datetime
from api import call_api
from book import Book


# MAIN BOOK FILTER FUNCTION
# Fetches books based on user input and criteria
def find_books(subject, book_length, start_year, end_year, order_by, min_results=10):
    results = []  # Initialise list to store results
    seen_books = set()  # Maintain a set of seen titles and authors so no repeats
    page = 0

    while (
        len(results) < min_results
    ):  # Keep the search/loop going until 10 books are found (pagination)
        items = call_api(subject, page, order_by)  # Fetch books from API

        for item in items:
            try:
                # Create book instance using the Book class
                book = Book(item)

                # 1st filter removes anything with missing data
                if any(
                    value == "N/A" or value == 0 for value in book.__dict__.values()
                ):
                    continue

                # 2nd filter check for duplicates to ensure unique books in the results
                book_id = get_book_id(book)
                if book_id in seen_books:
                    continue  # Skips over this book, as already been seen
                seen_books.add(book_id)  # If not already seen, adds it to the list

                # 3rd filter checks if there are any excluded categories and if rating is 4+
                if excluded_categories(book) or low_rating(book):
                    continue

                # 4th filter checks within date range and selected book length
                year = get_published_year(book)
                length = get_book_length(book)
                if (
                    book_in_date_range(year, start_year, end_year)
                    and length == book_length
                ):
                    # If the book gets through these filters it is added book to results
                    results.append(book)

            except KeyError:
                pass

        page += 1  # Moves to new page by adding a random number between 1-10

    for book in results:
        print(book)

    return results[:min_results]  # Returns 10 results (index 0-9)


# HELPER FUNCTIONS
# Pulls the title and authors from book dict to make an id
def get_book_id(book):
    return book.title, book.authors


# Checks the excluded words against those in the book's categories
# If any are found, it returns the book so they can be filtered out in the find_books function
def excluded_categories(book):
    excluded = {"young adult", "juvenile"}
    categories = book.categories.lower()
    return book if any(substring in categories for substring in excluded) else None


# Checks the book's rating is less than 4
# If less than 4, it returns True so they can again be filtered out in the main.py
def low_rating(book):
    return book.average_rating < 4


# Uses the published date and returns it as just the year to compare against user's input year
def get_published_year(book):
    try:
        datetime.strptime(book.published_date, "%Y-%m-%d")
        return int(book.published_date[:4])
    except ValueError:
        return 0


# Returns the page count as a word (short, medium, long) that can be compared to user's input length
def get_book_length(book):
    if book.page_count < 200:
        return "short"
    elif book.page_count <= 400:
        return "medium"
    else:
        return "long"


# Checks that the published year (from get_published_year function) is within user's range
def book_in_date_range(published_year, start_year, end_year):
    return start_year <= published_year <= end_year


# Changes publish date to be DD-MM-YYYY rather than YYYY-MM-DD
def formatted_date(book):
    try:
        unformatted_date = datetime.strptime(book.published_date, "%Y-%m-%d")
        formatted_date = unformatted_date.strftime("%d-%m-%Y")
        return formatted_date
    except ValueError:
        return "N/A"