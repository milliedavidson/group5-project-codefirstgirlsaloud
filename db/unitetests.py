import unittest
from model.book import Book
from datetime import datetime
from functions import (
    excluded_categories,
    low_rating,
    get_published_year,
    get_book_length,
    book_in_date_range,
)


class TestBookSearch(unittest.TestCase):

    # Testing if the excluded_categories function correctly identifies a book with the catergory "young adult" 
    # as an excluded category AND correctly identifies books with multiple catergories like "Fantasy, Romance"
    def test_excluded_categories(self):
        book_with_excluded_category = Book({
            "categories": "young adult"
        })
        book_without_excluded_category = Book({
            "categories": "Classics"
        })
        book_with_multiple_categories = Book({
            "categories": "Fantasy, Romance"
        }) 

        self.assertTrue(excluded_categories(book_with_excluded_category))
        self.assertFalse(excluded_categories(book_without_excluded_category))
        self.assertTrue(excluded_categories(book_with_multiple_categories))

    # Testing if the low_rating function correctly identifies a book with a low average rating (3.5)
    # as actually having a low rating AND a book with a high rating (above 4.0+) as not having a low rating.
    def test_low_rating(self):
        low_rated_book = Book({
            "average_rating": 3.5
        })
        high_rated_book = Book({
            "average_rating": 4.5
        })
        book_with_high_rating = Book({
            "average_rating": 4.8
        })
       
        self.assertTrue(low_rating(low_rated_book))
        self.assertFalse(low_rating(high_rated_book))
        self.assertFalse(low_rating(book_with_high_rating))

    # Testing if the get_published_year function correctly extracts the years (2018) and (2023)
    # from valid published dates ("2018-05-15" and "2023-08-22") -> just two random example dates.
    def test_get_published_year(self):
        book_with_valid_date = Book({
            "published_date": "2018-05-15"
        })
        book_with_valid_date = Book({
            "published_date": "2023-08-22"
        })
        book_with_invalid_date = Book({
            "published_date": "invalid-date"
        })

        self.assertEqual(get_published_year(book_with_valid_date), 2018)
        self.assertEqual(get_published_year(book_with_valid_date), 2023)
        self.assertEqual(get_published_year(book_with_invalid_date), 0)

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

    # Testing if the book_in_date_range function correctly identifies a book published in 2000
    # as within the date range (1990 to 2020) and a book published in 1970 as being outside the date range.
    def test_book_in_date_range(self):
        self.assertTrue(book_in_date_range(2000, 1990, 2020))
        self.assertFalse(book_in_date_range(1970, 1990, 2020))


if __name__ == '__main__':
    unittest.main()

