from application import create_app

# Create the app instance using the factory function
app = create_app()

# Runs application in file
if __name__ == "__main__":
    app.run(debug=True, port=5001)