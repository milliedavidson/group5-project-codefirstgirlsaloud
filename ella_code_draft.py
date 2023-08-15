import requests


def categorize_book(pages):
    if pages < 200:
        return "Short Book"
    elif 200 <= pages <= 400:
        return "Medium Book"
    else:
        return "Long Book"


def get_books_by_subject(subject, book_length, start_year, end_year, min_results=10):
    results = []
    seen_books = set()  # Maintain a set of seen titles and authors so no repeats

    page = 1
    while len(results) < min_results:  # Keep the search going until 10 books are found (pagination)

        endpoint = f"https://www.googleapis.com/books/v1/volumes?q={subject}&maxResults=10&printType=books&language=en&startIndex={page * 10}"
        response = requests.get(endpoint)
        data = response.json()

        for item in data.get('items', []):
            try:
                if ('volumeInfo' in item and
                        'averageRating' in item['volumeInfo'] and
                        item['volumeInfo']['averageRating'] >= 4):
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
                        book_info['pageCount'] = categorize_book(item['volumeInfo'].get('pageCount', 0))
                        results.append(book_info)

            except KeyError:
                pass

        page += 1

    return results[:min_results]