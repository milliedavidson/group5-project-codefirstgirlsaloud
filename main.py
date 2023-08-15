import requests
import time

start_time = time.time()

# Edit these to change the request criteria
user_input_subject = "fiction+fantasy"   # Can remove 'bestseller', change 'fiction' and 'thriller'
book_length_input = "medium"  # Choose from 'short', 'medium', 'long'
start_year_input = int("2010")  # Change to any year
end_year_input = int("2023")  # Change to any year
order_by_input = "relevance"  # Choose between 'relevance' or 'newest'


# Function to categorise books by length
def categorise_book(pages):
    if pages < 200:
        return "Short Book"
    elif 200 <= pages <= 400:
        return "Medium Book"
    else:
        return "Long Book"


# Function to call API endpoint
def get_books_by_subject(subject, book_length, start_year, end_year, order_by, min_results=10):
    results = []
    seen_books = set()  # Maintain a set of seen titles and authors so no repeats

    page = 1  # Starts search on page 1
    while len(results) < min_results:  # Keep the search going until 10 books are found (pagination)

        # Endpoint constructed with user input
        endpoint = f"https://www.googleapis.com/books/v1/volumes?q={subject}&maxResults=40&printType=books&language=en&startIndex={page * 10}&orderBy={order_by}"
        response = requests.get(endpoint)
        data = response.json()

        for item in data.get('items', []):
            try:
                # Check if the terms 'juvenile', 'children's' or 'young adult' is present in categories
                categories = item['volumeInfo'].get('categories', [])
                excluded_terms = ["juvenile", "children's", "young adult"]
                # Only continues if these terms are not present
                if not any(term in category.lower() for term in excluded_terms for category in categories):
                    # Next checks that the rating is above 4, if yes, continues
                    if ('volumeInfo' in item and
                            'averageRating' in item['volumeInfo'] and
                            item['volumeInfo']['averageRating'] > 3):
                        # Extracts information such as published year, book length etc
                        published_year = int(item['volumeInfo'].get('publishedDate', '0')[:4])
                        book_length_condition = (
                            book_length == "short" and item['volumeInfo'].get('pageCount', 0) < 200 or
                            book_length == "medium" and 200 <= item['volumeInfo'].get('pageCount', 0) <= 400 or
                            book_length == "long" and item['volumeInfo'].get('pageCount', 0) > 400
                        )
                        year_condition = start_year <= published_year <= end_year
                        title = item['volumeInfo'].get('title', 'N/A')
                        authors = ', '.join(item['volumeInfo'].get('authors', ['Unknown']))
                        book_identifier = (title, authors)

                        # And then checks if all of the below conditions are met
                        if book_length_condition and year_condition and book_identifier not in seen_books:
                            seen_books.add(book_identifier)
                            book_info = {}
                            book_info['title'] = title
                            book_info['authors'] = authors
                            book_info['publishedDate'] = item['volumeInfo'].get('publishedDate', 'N/A')
                            book_info['description'] = item['volumeInfo'].get('description', 'N/A')
                            book_info['categories'] = ', '.join(item['volumeInfo'].get('categories', ['N/A']))
                            book_info['averageRating'] = item['volumeInfo'].get('averageRating', 0)
                            book_info['price'] = item.get('saleInfo', {}).get('retailPrice', {}).get('amount', 'N/A')
                            book_info['thumbnail'] = item['volumeInfo']['imageLinks'].get('thumbnail', 'N/A')
                            book_info['pageCount'] = categorise_book(item['volumeInfo'].get('pageCount', 0))
                            results.append(book_info)

            except KeyError:
                pass

        page += 1  # Adds 1 to page count

    return results[:min_results]  # Returns 10 results (aka index 0-9)


# Calls the API endpoint function
books = get_books_by_subject(user_input_subject, book_length_input, start_year_input, end_year_input, order_by_input)

# Prints results
for book in books:
    print(f"Title: {book['title']}")
    print(f"Author: {book['authors']}")
    print(f"Published: {book['publishedDate']}")
    print(f"Description: {book['description']}")
    print(f"Categories: {book['categories']}")
    print(f"Rating: {book['averageRating']} stars")
    print(f"Price: £{book['price']}")
    print(f"Image: {book['thumbnail']}")
    print('=' * 40)


end_time = time.time()

elapsed_time = end_time - start_time
print(f"API request took {elapsed_time:.2f} seconds.")