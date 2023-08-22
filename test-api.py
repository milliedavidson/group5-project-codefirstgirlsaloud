import unittest
from unittest.mock import patch
from api import call_api


class TestCallApi(unittest.TestCase):
    def setUp(self):
        self.subject = "python"
        self.page = 1
        self.order_by = "relevance"
        self.expected_response = [{"title": "Book 1"}, {"title": "Book 2"}]

    @patch("requests.get")
    def test_call_api_with_valid_subject(self, mock_get):
        mock_data = {"items": self.expected_response}
        mock_get.return_value.json.return_value = mock_data

        response = call_api(self.subject, self.page, self.order_by)
        self.assertEqual(response, self.expected_response)

    def assert_invalid_input_raises_error(self, subject, page, order_by):
        with self.assertRaises(ValueError):
            call_api(subject, page, order_by)

    def test_call_api_with_invalid_subject(self):
        self.assert_invalid_input_raises_error("", self.page, self.order_by)

    def test_call_api_with_invalid_page(self):
        self.assert_invalid_input_raises_error(self.subject, -1, self.order_by)

    def test_call_api_with_invalid_order_by(self):
        self.assert_invalid_input_raises_error(self.subject, self.page, "")


if __name__ == "__main__":
    unittest.main()
