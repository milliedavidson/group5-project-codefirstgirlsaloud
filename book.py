def create_book_dict(item):
    book_dict = {
        "title": item["volumeInfo"].get("title", "N/A"),
        "authors": ", ".join(item["volumeInfo"].get("authors", ["Unknown"])),
        "published_date": item["volumeInfo"].get("publishedDate", "N/A"),
        "description": item["volumeInfo"].get("description", "N/A"),
        "categories": item["volumeInfo"].get("categories", ["N/A"]),
        "average_rating": item["volumeInfo"].get("averageRating", 0),
        "price": (item.get("saleInfo", {}).get("retailPrice", {}).get("amount", "N/A")),
        "thumbnail": item["volumeInfo"]["imageLinks"].get("thumbnail", "N/A"),
        "page_count": item["volumeInfo"].get("pageCount", 0),
    }
    return book_dict


def format_book_info(book_dict):
    return (
        f"Title: {book_dict['title']}\n"
        f"Author: {book_dict['authors']}\n"
        f"Published: {book_dict['published_date']}\n"
        f"Description: {book_dict['description']}\n"
        f"Categories: {', '.join(book_dict['categories'])}\n"
        f"Rating: {book_dict['average_rating']} stars\n"
        f"Price: £{book_dict['price']}\n"
        f"Image: {book_dict['thumbnail']}\n"
        f"{'=' * 40}"
    )
