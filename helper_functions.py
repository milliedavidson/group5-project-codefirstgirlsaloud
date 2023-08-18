from datetime import datetime


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


# Returns the necessary information for each book
def format_book_info(book_dict):
    return (
        f"Title: {book_dict['title']}\n"
        f"Author: {book_dict['authors']}\n"
        f"Published: {formatted_date(book_dict)}\n"
        f"Description: {book_dict['description']}\n"
        f"Categories: {', '.join(book_dict['categories'])}\n"
        f"Rating: {book_dict['average_rating']} stars\n"
        f"Length: {get_book_length(book_dict).capitalize()}, {book_dict['page_count']} pages\n"
        f"Image: {book_dict['thumbnail']}\n"
        f"{'=' * 40}"  # Remove later - just to break results in PyCharm
    )


# Prints the final book results
def format_and_print_books(book_results):
    for book in book_results:
        formatted_info = format_book_info(book)
        print(formatted_info)
