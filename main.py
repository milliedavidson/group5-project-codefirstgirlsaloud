from functions import (
    find_books,
    format_category_for_search
)

from input import (
    selected_genre,
    selected_category,
    selected_book_length,
    selected_min_published_date,
    selected_max_published_date,
    selected_order_by
)

print(f"Genre input: {selected_genre}")
print(f"Category input: {selected_category}")
print(f"Length input: {selected_book_length}")
print(f"Start year input: {selected_min_published_date}")
print(f"End year input: {selected_max_published_date}")
print(f"Order by input: {selected_order_by}")

formatted_category = format_category_for_search(selected_category, selected_genre)

books = find_books(
    formatted_category,
    selected_book_length,
    selected_min_published_date,
    selected_max_published_date,
    selected_order_by
)

