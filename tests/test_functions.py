"""
test_functions.py - Test cases for functions in the book search module

This module contains a series of test cases that validate the behavior of 
functions within the book search module.
"""

import unittest
from db.functions import format_date, get_book_length, order_results
from model.book import Book


class TestGetBookLength(unittest.TestCase):
    """
    Test cases for the `get_book_length` function
    """
    def setUp(self):
        self.book_short = Book({"volumeInfo": {
            "title": "Sample Title",
            "authors": ["Sample Authors"],
            "publishedDate": "N/A",
            "description": "N/A",
            "categories": ["Fiction"],
            "averageRating": "N/A",
            "imageLinks": {"thumbnail": "N/A"},
            "pageCount": 100,
            "previewLink": "N/A"
        }})

        self.book_medium = Book({"volumeInfo": {
            "title": "Sample Title",
            "authors": ["Sample Authors"],
            "publishedDate": "N/A",
            "description": "N/A",
            "categories": ["Non Fiction"],
            "averageRating": "N/A",
            "imageLinks": {"thumbnail": "N/A"},
            "pageCount": 350,
            "previewLink": "N/A"
        }})

        self.book_long = Book({"volumeInfo": {
            "title": "Sample Title",
            "authors": ["Sample Authors"],
            "publishedDate": "N/A",
            "description": "N/A",
            "categories": ["Non Fiction"],
            "averageRating": "N/A",
            "imageLinks": {"thumbnail": "N/A"},
            "pageCount": 550,
            "previewLink": "N/A"
        }})

    def test_short(self):
        """
        Test if the function correctly categorises a book with 100 pages as "short"
        """
        self.assertEqual(get_book_length(self.book_short), "short")

    def test_medium(self):
        """
        Test if the function correctly categorises a book with 350 pages as "medium"
        """
        self.assertEqual(get_book_length(self.book_medium), "medium")

    def test_long(self):
        """
        Test if the function correctly categorises a book with 550 pages as "long"
        """
        # book = Book({"page_count": 550})
        self.assertEqual(get_book_length(self.book_long), "long")


class TestOrderResults(unittest.TestCase):
    """
    Test cases for the `order_results` function
    """
    def setUp(self):
        self.book1 = Book({"volumeInfo": {
            "title": "Sample Title",
            "authors": ["Sample Authors"],
            "publishedDate": "2022-05-15",
            "description": "N/A",
            "categories": ["Fiction"],
            "averageRating": 4.5,
            "imageLinks": {"thumbnail": "N/A"},
            "pageCount": 100,
            "previewLink": "N/A"
        }})

        self.book2 = Book({"volumeInfo": {
            "title": "Sample Title",
            "authors": ["Sample Authors"],
            "publishedDate": "2023-01-20",
            "description": "N/A",
            "categories": ["Non Fiction"],
            "averageRating": 3.8,
            "imageLinks": {"thumbnail": "N/A"},
            "pageCount": 350,
            "previewLink": "N/A"
        }})

    def test_order_newest(self):
        """
        Test if the function correctly orders books by the newest published date
        """

        expected = [self.book2, self.book1]
        self.assertEqual(order_results("newest", [self.book1, self.book2]), expected)

    def test_order_top_rated(self):
        """
        Test if the function correctly orders books by their average rating,
        from highest to lowest
        """
        expected = [self.book1, self.book2]
        self.assertEqual(order_results("top rated", [self.book1, self.book2]), expected)


class TestFormatDate(unittest.TestCase):
    """
    Test cases for the `format_date` function
    """
    def setUp(self):
        self.book_date = Book({"volumeInfo": {
            "title": "Sample Title",
            "authors": ["Sample Authors"],
            "publishedDate": "2019-05-15",
            "description": "N/A",
            "categories": ["Fiction"],
            "averageRating": 4.5,
            "imageLinks": {"thumbnail": "N/A"},
            "pageCount": 100,
            "previewLink": "N/A"
        }})

        self.invalid_book_date = Book({"volumeInfo": {
            "title": "Sample Title",
            "authors": ["Sample Authors"],
            "publishedDate": "invalid",
            "description": "N/A",
            "categories": ["Fiction"],
            "averageRating": 4.5,
            "imageLinks": {"thumbnail": "N/A"},
            "pageCount": 100,
            "previewLink": "N/A"
        }})

    def test_valid_date(self):
        """
        Test if the function correctly formats a valid published date
        """
        self.assertEqual(format_date(self.book_date), "15-05-2019")

    def test_invalid_date(self):
        """
        Test if the function correctly handles an invalid published date
        """
        self.assertEqual(format_date(self.invalid_book_date), "N/A")


if __name__ == "__main__":
    unittest.main()
