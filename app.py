from application import app

app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'


if __name__ == "__main__":
    app.run(debug=True)