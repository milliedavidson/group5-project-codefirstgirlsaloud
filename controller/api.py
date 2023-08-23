"""
Module to interact with the Google Books API.
"""

import logging
import requests


class ApiError(Exception):
    """
    Exception raised when there is an error interacting with the API
    """


logger = logging.getLogger(__name__)


def call_api(subject, page, timeout=10):
    """
    Call API endpoint and return results.

    Parameters:
    subject (str): Search term
    page (int): Page number of results
    order_by (str): Sort order
    timeout (int): API request timeout in seconds

    Raises:
    ApiError: Custom exception for any API errors

    Returns:
    list: List of result items
    """

    if not isinstance(subject, str):
        raise TypeError("Subject must be a string")

    if not isinstance(page, int):
        raise TypeError("Page must be an integer")

    endpoint = (
        f"https://www.googleapis.com/books/v1/volumes?q={subject}"
        f"&maxResults=40&printType=books&language=en"
        f"&startIndex={page*40}&orderBy=relevance"
    )

    logger.info("Requesting URL: %s", endpoint)

    try:
        response = requests.get(endpoint, timeout=timeout)
        response.raise_for_status()

        logger.info("API request succeeded, status code %s", response.status_code)

    except requests.exceptions.RequestException as error:
        raise ApiError from error

    if response.status_code == 404:
        return []

    data = response.json()
    return data.get("items", [])
