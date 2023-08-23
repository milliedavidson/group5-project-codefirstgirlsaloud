from datetime import datetime
from controller.api import call_api
from model.book import Book


# MAIN BOOK FILTER FUNCTION
# Fetches books based on user input and criteria
def find_books(
    selected_genre, selected_category, book_length, order_by, min_results=10
):
    results = []  # Initialise list to store results
    seen_books = set()  # Maintain a set of seen titles and authors so no duplicates
    page = 0
    empty_pages = 0

    while len(results) < min_results:
        items = call_api(selected_category, page)  # Fetch books from API
        if not items:
            empty_pages += 1
            if (
                empty_pages == 5
            ):  # When there have been 5 pages in a row with no results the loop ends
                break
        else:
            empty_pages = 0

        for item in items:
            try:
                # Create book instance using the Book class
                book = Book(item)

                # 1st filter removes anything with missing data
                if any(
                    value == "N/A" for value in book.__dict__.values()
                ):
                    continue

                # 2nd filter check for duplicates to ensure unique books in the results
                book_id = get_book_id(book)
                if book_id in seen_books:
                    continue  # Skips over this book, as already been seen
                seen_books.add(book_id)  # If not already seen, adds it to the list

                # 3rd filter checks if there are any excluded categories
                if excluded_categories(book, selected_genre, selected_category):
                    continue

                # 4th filter checks for selected book length
                # year = get_published_year(book)
                length = get_book_length(book)
                if length == book_length:
                    # If the book gets through this filter it is added book to results
                    results.append(book)

                    if len(results) == min_results:  # Stops when 10 are found
                        break

            except KeyError:
                pass

        page += 1  # Moves to new page by adding a random number between 1-10

        # 5th filter to sort results based on user selection
        sorted_results = order_results(order_by, results)

        return sorted_results[:min_results]  # Returns 10 results (index 0-9)


# HELPER FUNCTIONS
# Pulls the title and authors from book dict to make an id
def get_book_id(book):
    return book.title, book.authors


# If fiction - ensures that book.categories is also fiction
# If non-fiction - ensures that book.categories is the selected_category e.g. cooking
# When a book is found that doesn't match these conditions, it is returned + filtered out in the find_books function
def excluded_categories(book, selected_genre, selected_category):
    if selected_genre == "fiction":
        if book.categories.lower() != selected_genre:
            return book
    else:  # (if selected_genre == "non-fiction")
        if book.categories.lower() != selected_category.lower():
            return book


# Formats category for better API endpoint results
# If fiction "q=fiction+selected_category"
# If non-fiction "q=selected_category"
def format_category_for_search(selected_category, selected_genre):
    if selected_genre == "fiction":
        formatted_category = "fiction+" + selected_category
    else:
        formatted_category = selected_category
    return formatted_category


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


# Changes publish date to be DD-MM-YYYY rather than YYYY-MM-DD
def formatted_date(book):
    try:
        unformatted_date = datetime.strptime(book.published_date, "%Y-%m-%d")
        formatted_date = unformatted_date.strftime("%d-%m-%Y")
        return formatted_date
    except ValueError:
        return "N/A"


# Formats the published date for HTML
def format_book_published(book):
    return f"{formatted_date(book)}\n"


# Formats the rating for HTML
def format_book_rating(book):
    book_rating = book.average_rating
    if book_rating == 0:
        return "No ratings yet"
    else:
        return f"{book_rating} stars"


# Formats the book length for HTML
def format_book_length(book):
    return f"{get_book_length(book).capitalize()}, {book.page_count} pages"


# Sorts the results based on the order_by user input selection
def order_results(order_by, results):
    sorted_results = []

    if order_by == "newest":
        sorted_results = sorted(
            results,
            key=lambda book: datetime.strptime(book.published_date, "%Y-%m-%d"),
            reverse=True,
        )

    elif order_by == "top rated":
        sorted_results = sorted(
            results, key=lambda book: int(book.average_rating), reverse=True
        )

    return sorted_results
