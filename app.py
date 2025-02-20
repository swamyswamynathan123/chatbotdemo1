import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify


# Load environment variables
load_dotenv()


# Initialize Flask app
app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')




# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)