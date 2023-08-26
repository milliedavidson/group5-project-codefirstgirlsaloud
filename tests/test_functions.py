"""
test_functions.py - Test cases for functions in the book search module

This module contains a series of test cases that validate the behavior of 
functions within the book search module.
"""

import unittest
from db.functions import format_date, get_book_length, order_results, excluded_categories
from model.book import Book


class TestBookSearch(unittest.TestCase):
    """
    Test cases for the `excluded_categories` function
    """

    def test_excluded_categories_fiction(self):
        """
        Test if the function correctly filters out excluded categories for the fiction genre
        """
        book_fiction = Book({"categories": "Fiction"})
        book_nonfiction = Book({"categories": "Non-Fiction"})

        self.assertEqual(
            excluded_categories(book_fiction, "fiction", "Some Category"), None
        )
        self.assertEqual(
            excluded_categories(book_fiction, "fiction", "Another Category"),
            book_fiction,
        )
        self.assertEqual(
            excluded_categories(book_nonfiction, "fiction", "Some Category"),
            book_nonfiction,
        )

    def test_excluded_categories_nonfiction(self):
        """
        Test if the function correctly filters out excluded categories for the non-fiction genre
        """
        book_fiction = Book({"categories": "Fiction"})
        book_nonfiction = Book({"categories": "Non-Fiction"})

        self.assertEqual(
            excluded_categories(book_nonfiction, "non-fiction", "Some Category"), None
        )
        self.assertEqual(
            excluded_categories(book_nonfiction, "non-fiction", "Another Category"),
            None,
        )
        self.assertEqual(
            excluded_categories(book_fiction, "non-fiction", "Some Category"),
            book_fiction,
        )


class TestGetBookLength(unittest.TestCase):
    """
    Test cases for the `get_book_length` function
    """

    def test_short(self):
        """
        Test if the function correctly categorises a book with 100 pages as "short"
        """
        book = Book({"page_count": 100})
        self.assertEqual(get_book_length(book), "short")

    def test_medium(self):
        """
        Test if the function correctly categorises a book with 350 pages as "medium"
        """
        book = Book({"page_count": 350})
        self.assertEqual(get_book_length(book), "medium")

    def test_long(self):
        """
        Test if the function correctly categorises a book with 550 pages as "long"
        """
        book = Book({"page_count": 550})
        self.assertEqual(get_book_length(book), "long")


class TestOrderResults(unittest.TestCase):
    """
    Test cases for the `order_results` function
    """

    def test_order_newest(self):
        """
        Test if the function correctly orders books by the newest published date
        """
        book1 = Book({"published_date": "2022-05-15"})
        book2 = Book({"published_date": "2023-01-20"})
        expected = [book2, book1]
        self.assertEqual(order_results("newest", [book1, book2]), expected)

    def test_order_top_rated(self):
        """
        Test if the function correctly orders books by their average rating,
        from highest to lowest
        """
        book1 = Book({"average_rating": 4.5})
        book2 = Book({"average_rating": 3.8})
        expected = [book1, book2]
        self.assertEqual(order_results("top rated", [book1, book2]), expected)


class TestFormatDate(unittest.TestCase):
    """
    Test cases for the `format_date` function
    """

    def test_valid_date(self):
        """
        Test if the function correctly formats a valid published date
        """
        book = Book({"published_date": "2019-05-15"})
        self.assertEqual(format_date(book), "15-05-2019")

    def test_invalid_date(self):
        """
        Test if the function correctly handles an invalid published date
        """
        book = Book({"published_date": "invalid"})
        self.assertEqual(format_date(book), "N/A")


if __name__ == "__main__":
    unittest.main()
