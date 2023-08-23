from functions import (
    find_books
)

from input import (
    selected_genre,
    formatted_category,
    selected_book_length,
    selected_min_published_date,
    selected_max_published_date,
    selected_order_by
)

print(f"Genre input: {selected_genre}")
print(f"Category input: {formatted_category}")
print(f"Length input: {selected_book_length}")
print(f"Start year input: {selected_min_published_date}")
print(f"End year input: {selected_max_published_date}")
print(f"Order by input: {selected_order_by}")


books = find_books(
    formatted_category,
    selected_book_length,
    selected_min_published_date,
    selected_max_published_date,
    selected_order_by
)

