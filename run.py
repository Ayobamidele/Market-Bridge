from api import create_app

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # Run the application with debug mode enabled
    app.run(debug=True)
