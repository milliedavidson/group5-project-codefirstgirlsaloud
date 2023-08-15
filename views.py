from flask import Flask, jsonify, request
# from draft import get_books_by_subject
# from draft_config import MY_API_KEY

app = Flask(__name__)


@app.route('/')
def index():
    with open('home.html', 'r') as file:
        return file.read()


@app.route('/process', methods=['POST'])
def process():
    # selected_genre = request.form['genres']
    selected_category = request.form['categories']
    selected_book_length = request.form['book_length']
    selected_min_published_date = int(request.form['year_published_min'])
    selected_max_published_date = int(request.form['year_published_max'])
    # You can now use the 'selected_' values in your Python code
    return f'''
    Category: {selected_category}
    Book Length: {selected_book_length}
    Published Between: {selected_min_published_date} - {selected_max_published_date}
'''


# @app.route('/results/<subject>')
# def display_books(subject):
#     print('API SERVER SAYS:', subject)
#     res = get_books_by_subject(subject, MY_API_KEY)
#     return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, port=5001)