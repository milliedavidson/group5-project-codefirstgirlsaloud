def get_book_id(book_dict):
    return book_dict["title"], book_dict["authors"]


def is_excluded_category(book_dict):
    excluded = ["young adult fiction", "juvenile fiction"]
    lowercase_excluded = [cat.lower() for cat in excluded]
    lowercase_categories = [cat.strip().lower() for cat in book_dict["categories"]]
    result = any(cat in lowercase_excluded for cat in lowercase_categories)
    return result


def rating_too_low(book_dict):
    return book_dict["average_rating"] < 4


def get_published_year(book_dict):
    published_date = book_dict["published_date"]
    if published_date is None or published_date == "N/A":
        return None
    return int(published_date[:4])


def book_in_date_range(published_year, start_year, end_year):
    return start_year <= published_year <= end_year


def get_book_length(book_dict):
    if book_dict["page_count"] < 200:
        return "short"
    elif book_dict["page_count"] <= 400:
        return "medium"
    else:
        return "long"


def book_matches_length(desired_book_length, book_dict):
    book_length = get_book_length(book_dict)
    return book_length == desired_book_length
