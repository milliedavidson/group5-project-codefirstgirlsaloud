"""
Book filtering module

Fetch, filter and format books from API based on user criteria
"""

import traceback
from datetime import datetime

from controller.api import call_api
from model.book import Book

# Constants
MAX_EMPTY_PAGES = 5


# Enums
class BookLength:
    """
    Enumeration for different book lengths.

    Attributes:
        SHORT: Represents a short book.
        MEDIUM: Represents a medium-length book.
        LONG: Represents a long book.
    """

    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"


# MAIN FUNCTION
def find_books(subject, book_length, start_year, end_year, min_results=10):
    """
    Find and return a list of books matching the criteria

    Params:
        search_query: Keyword(s) to search books API
        desired_length: Length category - 'short', 'medium', or 'long'
        start_year: Minimum published year
        end_year: Maximum published year
        min_results: Minimum number of results to return

    Returns:
        List of Book objects matching criteria, up to min_results
    """

    results = []  # Initialise list to store results
    seen_books = set()  # Maintain a set of seen titles and authors so no duplicates
    page = 0
    empty_pages = 0

    while len(results) < min_results:
        items = call_api(subject, page)  # Fetch books from API
        if not items:
            empty_pages += 1
            if (
                empty_pages == MAX_EMPTY_PAGES
            ):  # After 5 pages in a row with no results, the loop ends
                break

        else:
            empty_pages = 0

        for item in items:
            try:
                # Create book instance using the Book class
                book = Book(item)

                # 1st filter removes anything with missing data
                if any(
                    value == "N/A" or value == 0 for value in book.__dict__.values()
                ):
                    continue

                # 2nd filter checks for duplicates to ensure unique books in the results
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
                # Catches KeyError exceptions and prints the error message
                traceback.print_exc()

        page += 1  # Moves to new page by adding a random number between 1-10

    for book in results:
        print(book)

    return results[:min_results]  # Returns 10 results (index 0-9)


# Custom exceptions
class BookAttributeError(Exception):
    """
    Raised when a book attribute is invalid or missing.

    Attributes:
        message -- explanation of the error
    """


class BookDataError(Exception):
    """
    Raised when book data is invalid or cannot be processed.

    Attributes:
        message -- explanation of the error
    """


# HELPER FUNCTIONS
def get_book_id(book):
    """Pulls the title and authors from book dict to make an id"""
    try:
        return book.title, book.authors
    except AttributeError as exc:
        raise BookAttributeError("Could not get book ID attributes") from exc


def excluded_categories(book):
    """
    Checks the excluded words against those in the book's categories

    If any are found, it returns the book so they can be filtered out in the find_books function
    """
    excluded = {"young adult", "juvenile"}
    try:
        categories = book.categories.lower()
        return book if any(substring in categories for substring in excluded) else None
    except AttributeError:
        traceback.print_exc()
        return None


def low_rating(book):
    """
    Checks the book's rating is less than 4

    If less than 4, it returns True so they can again be filtered out in the main.py
    """
    try:
        return book.average_rating < 4
    except AttributeError:
        traceback.print_exc()
        return False


def get_published_year(book):
    """
    Uses the published date and returns it as just the
    year to compare against user's input year
    """
    try:
        return int(book.published_date[:4])
    except (AttributeError, ValueError) as exc:
        raise BookDataError("Invalid publish date format") from exc


def get_book_length(book):
    """
    Returns the page count as a word (short, medium, long)
    that can be compared to user's input length
    """
    try:
        if book.page_count < 200:
            return BookLength.SHORT
        elif book.page_count <= 400:
            return BookLength.MEDIUM
        else:
            return BookLength.LONG
    except AttributeError:
        traceback.print_exc()
        return None


def book_in_date_range(published_year, start_year, end_year):
    """
    Checks that the published year
    (from get_published_year function) is within user's range
    """
    try:
        return start_year <= published_year <= end_year
    except TypeError:
        traceback.print_exc()
        return False


def format_date(book):
    """Changes publish date to be DD-MM-YYYY rather than YYYY-MM-DD"""
    try:
        unformatted_date = datetime.strptime(book.published_date, "%Y-%m-%d")
        formatted_date = unformatted_date.strftime("%d-%m-%Y")
        return formatted_date
    except (AttributeError, ValueError):
        traceback.print_exc()
        return "N/A"


def format_book_published(book):
    """Formats the published date for HTML"""
    return f"{format_date(book)}\n"


def format_book_categories(book):
    """Formats the categories for HTML"""
    try:
        return book.categories
    except AttributeError:
        traceback.print_exc()
        return "N/A"


def format_book_rating(book):
    """Formats the rating for HTML"""
    try:
        return f"{book.average_rating} stars"
    except AttributeError:
        traceback.print_exc()
        return "N/A"


def format_book_length(book):
    """Formats the book length for HTML"""
    try:
        length = get_book_length(book)
        if length:
            return f"{length.capitalize()}, {book.page_count} pages"
        else:
            return "N/A"
    except AttributeError:
        traceback.print_exc()
        return "N/A"


def format_category_for_search(category, selected_genre):
    """Formats the book length for HTML"""
    try:
        if selected_genre == "fiction":
            formatted_category = "fiction+" + category
        else:
            formatted_category = category
        return formatted_category
    except AttributeError:
        traceback.print_exc()
        return "N/A"
