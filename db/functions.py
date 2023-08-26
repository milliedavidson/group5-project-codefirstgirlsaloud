"""
Book filtering module

Fetch, filter and format books from API based on user criteria
"""

import traceback
from datetime import datetime

from controller.api import call_api
from model.book import Book


# Custom exceptions
class ApiError(Exception):
    """
    Exception raised for errors related to API interactions.

    Attributes:
        message -- explanation of the error
    """


class ParsingError(Exception):
    """
    Exception raised for errors during data parsing.

    Attributes:
        message -- explanation of the error
    """


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
def find_books(
    selected_genre, selected_category, selected_book_length, order_by, min_results=10
):
    """
    Find and return a list of books matching the criteria

     Params:
        selected_genre: Selected genre ('fiction' or 'non-fiction')
        selected_category: Selected category for filtering
        selected_book_length: Desired book length category
        order_by: Sorting criterion ('newest' or 'top rated')
        min_results: Minimum number of results to return

    Returns:
        List of Book objects matching criteria, up to min_results
    """

    results = []  # Initialise list to store results
    seen_books = set()  # Maintain a set of seen titles and authors so no duplicates
    page = 0
    empty_pages = 0

    while len(results) < min_results:
        try:
            called_book_data = call_api(selected_category, page)  # Fetch books from API
        except ApiError:
            print("Error calling API")
            return []

        # Checks if page is empty
        if not called_book_data:
            empty_pages += 1
            if (
                empty_pages == 100
            ):  # When there have been 5 pages in a row with no results the loop ends
                break

        # For each item from those from API endpoint:
        for item in called_book_data:
            try:
                # Create book instance using the Book class
                book = Book(item)

                # 1st filter removes anything with missing data - other than a 0 rating
                if any(value == "N/A" for value in book.__dict__.values()):
                    continue

                # 2nd filter check for duplicates to ensure unique books in the results
                book_id = get_book_id(book)
                if book_id in seen_books:
                    continue  # Skips over this book, as already been seen
                seen_books.add(book_id)  # If not already seen, adds it to the list

                # 3rd filter checks if there are any excluded categories
                if excluded_categories(book, selected_genre, selected_category):
                    continue

                # 4th filter checks for selected book length and correctly formatted date
                book_length = get_book_length(book)
                date = format_date(book)
                if book_length == selected_book_length and date != "N/A":
                    # If the book gets through this filter it is added book to results
                    results.append(book)

                    if len(results) == min_results:  # Stops when 10 are found
                        break

            # Catches KeyErrors & ParsingErrors and prints the error message
            except (KeyError, ParsingError) as exception:
                print("Error processing book data: ", exception)

        page += 1  # Moves to new page

        # Calls function to sort final results based on user selection
        sorted_results = order_results(order_by, results)

        return sorted_results[:min_results]  # Returns 10 results (index 0-9)


# HELPER FUNCTIONS
def get_book_id(book):
    """
    Pulls the title and authors from book dict to make an id
    """
    try:
        return book.title, book.authors
    except AttributeError as exc:
        raise BookAttributeError("Could not get book ID attributes") from exc


def excluded_categories(book, selected_genre, selected_category):
    """
    If fiction - ensures that book.categories is also fiction
    If non-fiction - compares against certain excluded categories to ensure accurate results
    When a book is found that doesn't match these conditions,
    it is returned + filtered out in the find_books function
    """
    if selected_genre == "fiction":
        if book.categories.lower() != selected_genre:
            return book
    else:  # (if selected_genre == "non-fiction")
        excluded = {"young adult", "juvenile", "fiction"}
        return (
            book
            if any(substring in book.categories.lower() for substring in excluded)
            else None
        )


def format_category_for_search(selected_category, selected_genre):
    """
    Formats category for better API endpoint results
    If fiction and science fiction "q=sciencefiction"
    If fiction "q=fiction+selected_category"
    If fiction and one of a selected list "q=subject:selected_category"
    If non-fiction "q=selected_category"
    """
    nonfiction_subject_list = ["Gardening", "Music", "Nature", "Philosophy", "Religion"]

    if selected_genre == "fiction" and selected_category == "Science Fiction":
        return selected_category.replace(" ", "")

    if selected_genre == "fiction":
        formatted_category = "fiction+" + selected_category.replace(" ", "")

    elif (
        selected_genre == "non-fiction" and selected_category in nonfiction_subject_list
    ):
        formatted_category = "subject:" + selected_category

    else:
        formatted_category = selected_category.replace(" ", "")

    return formatted_category


def get_book_length(book):
    """
    Returns the page count as a word (short, medium, long)
    that can be compared to user's input length
    """
    try:
        if book.page_count < 200:
            return "short"
        elif book.page_count <= 400:
            return "medium"
        else:
            return "long"
    except AttributeError as exc:
        raise BookDataError("Could not get book length") from exc


def format_date(book):
    """
    Changes publish date to be DD-MM-YYYY rather than YYYY-MM-DD
    """
    try:
        unformatted_date = datetime.strptime(book.published_date, "%d-%m-%Y")
        return book.published_date  # If already in the correct format, return as is
    except ValueError:
        try:
            unformatted_date = datetime.strptime(book.published_date, "%Y-%m-%d")
            formatted_date = unformatted_date.strftime("%d-%m-%Y")
            return formatted_date
        except (AttributeError, ValueError):
            traceback.print_exc()
            return "N/A"


def format_book_published(book):
    """
    Formats the published date for HTML
    """
    return f"{format_date(book)}\n"


def format_book_rating(book):
    """
    Formats the rating for HTML
    """
    try:
        book_rating = book.average_rating
        if book_rating == 0:
            return "No ratings yet"
        else:
            return f"{book_rating} stars"
    except AttributeError:
        traceback.print_exc()
        return "N/A"


def format_book_length(book):
    """
    Formats the book length for HTML
    """
    return f"{get_book_length(book).capitalize()}, {book.page_count} pages"


def order_results(order_by, results):
    """
    Sorts the results based on the order_by user input selection
    """
    sorted_results = []

    if order_by == "newest":
        sorted_results = sorted(
            results,
            key=lambda book: datetime.strptime(format_date(book), "%d-%m-%Y"),
            reverse=True,
        )

    elif order_by == "top rated":
        sorted_results = sorted(
            results, key=lambda book: float(book.average_rating), reverse=True
        )

    return sorted_results
