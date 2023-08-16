def is_excluded_category(book):
    excluded = ["juvenile", "children", "young adult"]
    return any(cat in excluded for cat in book.categories)


def rating_too_low(book):
    return book.average_rating <= 3


def get_published_year(book):
    return int(book.published_date[:4])


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