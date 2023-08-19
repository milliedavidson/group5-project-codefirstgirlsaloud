from datetime import datetime
import random
from api import call_api
from book import create_book_dict


# MAIN BOOK FILTER FUNCTION
# Fetches books based on user input and criteria
def find_books(subject, book_length, start_year, end_year, order_by, min_results=10):
    results = []  # Initialise list to store results
    seen_books = set()  # Maintain a set of seen titles and authors so no repeats
    page = random.randint(0, 10)  # Starts search on random page number between 0-10

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


# HELPER FUNCTIONS
# Pulls the title and authors from book dict to make an id
def get_book_id(book_dict):
    return book_dict["title"], book_dict["authors"]


# Checks the excluded words against those in the books categories
# If any are found it returns them, so they can be filtered out in the main.py
def excluded_categories(book_dict):
    excluded = {"young adult fiction", "juvenile fiction"}
    categories = [cat.lower().strip() for cat in book_dict["categories"]]
    return any(cat in excluded for cat in categories)


# Checks the books rating is greater than 4
# If less than 4 it returns them, so they can again be filtered out in the main.py
def low_rating(book_dict):
    return book_dict["average_rating"] < 4


# Uses the published date and returns it as just the year to compare against users input year
def get_published_year(book_dict):
    published_date = book_dict["published_date"]
    return int(published_date[:4])


# Returns the page count as a word (short, medium, long) that can be compared to user input length
def get_book_length(book_dict):
    if book_dict["page_count"] < 200:
        return "short"
    elif book_dict["page_count"] <= 400:
        return "medium"
    else:
        return "long"


# Checks that the published year (from get_published_year function) is within users range
def book_in_date_range(published_year, start_year, end_year):
    return start_year <= published_year <= end_year


# Changes publish date to be DD-MM-YYYY rather than YYYY-MM-DD
def formatted_date(book_dict):
    unformatted_date = datetime.strptime(book_dict["published_date"], "%Y-%m-%d")
    formatted_date = unformatted_date.strftime("%d-%m-%Y")
    return formatted_date


# Formats the published date for html
def format_book_published(book_dict):
    return f"{formatted_date(book_dict)}\n"


# Formats the categories for html
def format_book_categories(book):
    return ', '.join(book['categories'])


# Formats the rating for html
def format_book_rating(book):
    return f"{book['average_rating']} stars"


# Formats the book length for html
def format_book_length(book):
    return f"{get_book_length(book).capitalize()}, {book['page_count']} pages"

