import os  # Import the os module

from flask import Flask  # Make sure to import Flask

app = Flask(__name__)

# Define your routes here
@app.route('/')
def home():
    return "Hello, welcome to my API!"

# Get the port from the environment variable or default to 5000
port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    # Run the app on the specified port
    app.run(host='0.0.0.0', port=port)
