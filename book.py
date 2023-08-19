# Creates a book dictionary - this is where all the data is pulled from
def create_book_dict(item):
    book_dict = {
        "title": item["volumeInfo"].get("title", "N/A"),
        "authors": ", ".join(item["volumeInfo"].get("authors", "N/A")),
        "published_date": item["volumeInfo"].get("publishedDate", "N/A"),
        "description": item["volumeInfo"].get("description", "N/A"),
        "categories": item["volumeInfo"].get("categories", "N/A"),
        "average_rating": item["volumeInfo"].get("averageRating", 0),
        "price": (item.get("saleInfo", {}).get("retailPrice", {}).get("amount", "N/A")),
        "thumbnail": item["volumeInfo"]["imageLinks"].get("thumbnail", "N/A"),
        "page_count": item["volumeInfo"].get("pageCount", 0)
    }
    return book_dict
