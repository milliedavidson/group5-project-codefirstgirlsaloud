class Book:
    def __init__(self, item):
        self.title = item["volumeInfo"].get("title", "N/A")
        self.authors = ", ".join(item["volumeInfo"].get("authors", ["Unknown"]))
        self.published_date = item["volumeInfo"].get("publishedDate", "N/A")
        self.description = item["volumeInfo"].get("description", "N/A")
        self.categories = ", ".join(item["volumeInfo"].get("categories", ["N/A"]))
        self.average_rating = item["volumeInfo"].get("averageRating", 0)
        self.price = (
            item.get("saleInfo", {}).get("retailPrice", {}).get("amount", "N/A")
        )
        self.thumbnail = item["volumeInfo"]["imageLinks"].get("thumbnail", "N/A")
        self.page_count = item["volumeInfo"].get("pageCount", 0)

    def __str__(self):
        return (
            f"Title: {self.title}\n"
            f"Author: {self.authors}\n"
            f"Published: {self.published_date}\n"
            f"Description: {self.description}\n"
            f"Categories: {self.categories}\n"
            f"Rating: {self.average_rating} stars\n"
            f"Price: £{self.price}\n"
            f"Image: {self.thumbnail}\n"
            f"{'=' * 40}"
        )

    def get_book_id(self):
        return self.title, self.authors