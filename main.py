from application import app

app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

# moved all routing code to routes.py file

if __name__ == '__main__':
    app.run(debug=True, port=5001)

