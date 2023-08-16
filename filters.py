def get_book_id(book):
    return book.title, book.authors


def is_excluded_category(book):
    excluded = ["young adult fiction", "juvenile fiction"]
    lowercase_excluded = [cat.lower() for cat in excluded]
    lowercase_categories = [cat.strip().lower() for cat in book.categories.split(',')]  # Convert to lowercase
    result = any(cat in lowercase_excluded for cat in lowercase_categories)
    return result


def rating_too_low(book):
    return book.average_rating < 4


def get_published_year(book):
    published_date = book.published_date
    if published_date is None or published_date == 'N/A':
        return None  # Return None for books with missing or invalid published date
    return int(published_date[:4])


def book_in_date_range(
    published_year,
    start_year,
    end_year,
):
    return start_year <= published_year <= end_year


def get_book_length(book):
    if book.page_count < 200:
        return "short"
    elif book.page_count <= 400:
        return "medium"
    else:
        return "long"


def book_matches_length(book, desired_book_length):
    return book.length == desired_book_length



# USEFUL FOR TESTING CATEGORIES/CHANGING REQUIREMENTS
# def is_excluded_category(book):
#     excluded = ["young adult fiction", "juvenile fiction"]
#     lowercase_excluded = [cat.lower() for cat in excluded]
#     lowercase_categories = [cat.strip().lower() for cat in book.categories.split(',')]  # Convert to lowercase
#
#     print("Lowercase Excluded Categories:", lowercase_excluded)
#     print("Lowercase Book Categories:", lowercase_categories)
#
#     result = any(cat in lowercase_excluded for cat in lowercase_categories)
#     print("Result:", result)
#
#     return result