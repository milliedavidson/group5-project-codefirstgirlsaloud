"""
test_api.py - Test cases for the call_api function

This module contains a unittest test suite with test cases for validating 
the call_api function behavior and input validation. The tests mock the 
API response and assert on the function output.
"""


import unittest
from unittest.mock import patch
from controller.api import call_api


class TestCallApi(unittest.TestCase):
    """
    A test suite for the `call_api` function in the `controller.api` module
    """

    def setUp(self):
        """
        Initialize common test data for the test cases
        """
        self.subject = "python"
        self.page = 1
        self.order_by = "relevance"
        self.expected_response = [{"title": "Book 1"}, {"title": "Book 2"}]

    @patch("requests.get")
    def test_call_api_with_valid_subject(self, mock_get):
        """
        Test the `call_api` function with valid input subject
        """
        mock_data = {"items": self.expected_response}
        mock_get.return_value.json.return_value = mock_data

        response = call_api(self.subject, self.page, timeout=10)
        self.assertEqual(response, self.expected_response)

    def assert_invalid_input_raises_error(self, subject, page, order_by):
        """
        Helper method to assert that invalid input raises a ValueError
        """
        with self.assertRaises(ValueError):
            call_api(subject, page, order_by)

    def test_call_api_with_invalid_subject(self):
        """
        Test the `call_api` function with an invalid empty subject
        """
        self.assert_invalid_input_raises_error("", self.page, self.order_by)

    def test_call_api_with_invalid_page(self):
        """
        Test the `call_api` function with an invalid negative page number
        """
        self.assert_invalid_input_raises_error(self.subject, -1, self.order_by)

    def test_call_api_with_invalid_order_by(self):
        """
        Test the `call_api` function with an invalid empty order_by value
        """
        self.assert_invalid_input_raises_error(self.subject, self.page, "")


if __name__ == "__main__":
    unittest.main()
