import unittest
from db.functions import format_date, order_results
from model.book import Book
from datetime import datetime
from functions import (
    find_books,
    excluded_categories,
    get_book_length,
    order_results,
)

class TestBookSearch(unittest.TestCase):
    
    # Testing if the excluded_categories function works correctly filters out 
    # excluded categories based on the selected genre.
    def test_excluded_categories_fiction(self):
        
        book_fiction = Book({
            "categories": "Fiction"
        })
        book_nonfiction = Book({
            "categories": "Non-Fiction"
        })

        self.assertEqual(excluded_categories(book_fiction, "fiction", "Some Category"), None)
        self.assertEqual(excluded_categories(book_fiction, "fiction", "Another Category"), book_fiction)
        self.assertEqual(excluded_categories(book_nonfiction, "fiction", "Some Category"), book_nonfiction)

    # Testing if the excluded_categories function works correctly for the non-fiction genre.
    def test_excluded_categories_nonfiction(self):
        
        book_fiction = Book({
            "categories": "Fiction"
        })
        book_nonfiction = Book({
            "categories": "Non-Fiction"
        })

        self.assertEqual(excluded_categories(book_nonfiction, "non-fiction", "Some Category"), None)
        self.assertEqual(excluded_categories(book_nonfiction, "non-fiction", "Another Category"), None)
        self.assertEqual(excluded_categories(book_fiction, "non-fiction", "Some Category"), book_fiction)

    # Testing if the get_book_length function correctly categorises a book with 100 pages
    # as "short", a book with 350 pages as "medium", and a book with 550 pages as "long".
    def test_get_book_length(self):
        short_book = Book({
            "page_count": 100
        })
        medium_book = Book({
            "page_count": 350
        })
        long_book = Book({
            "page_count": 550
        })

        self.assertEqual(get_book_length(short_book), "short")
        self.assertEqual(get_book_length(medium_book), "medium")
        self.assertEqual(get_book_length(long_book), "long")

    # Testing if the order_results function correctly orders books by the newest published date.
    def test_order_results_newest(self):
        book_1 = Book({
            "published_date": "2022-05-15",
            "average_rating": 4.5
        })
        book_2 = Book({
            "published_date": "2023-01-20",
            "average_rating": 3.8
        })

        self.assertEqual(order_results("newest", [book_1, book_2]), [book_2, book_1])
    
    # Testing if the order_results function correctly orders books by their average
    # rating, from highest to lowest.
    def test_order_results_top_rated(self):   
        book_1 = Book({
            "published_date": "2022-05-15",
            "average_rating": 4.5
        })
        book_2 = Book({
            "published_date": "2023-01-20",
            "average_rating": 3.8
        })

        self.assertEqual(order_results("top rated", [book_1, book_2]), [book_1, book_2])
    
    # Testing to see if the formatted_date function correctly formats published dates
    # and handles cases where the date might be invalid.
    def test_formatted_date(self):
        
        book_with_valid_date = Book({
            "published_date": "2019-05-15"
        })
        book_with_invalid_date = Book({
            "published_date": "invalid-date"
        })

        self.assertEqual(format_date(book_with_valid_date), "15-05-2019")
        self.assertEqual(format_date(book_with_invalid_date), "N/A")

if __name__ == '__main__':
    unittest.main()

