from application import app

# moved all routing code to routes.py file

if __name__ == "__main__":
    app.run(debug=True, port=5001)
