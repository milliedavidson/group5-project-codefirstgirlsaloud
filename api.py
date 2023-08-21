import requests


# Function to call API endpoint
def call_api(subject, page, order_by):
    endpoint = f"https://www.googleapis.com/books/v1/volumes?q={subject}&maxResults=40&printType=books&language=en&startIndex={page*40}&orderBy={order_by}"
    response = requests.get(endpoint)
    data = response.json()
    print(endpoint)
    return data.get("items", [])
