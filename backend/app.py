import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
from flask_cors import CORS
from db import init_db, close_connection

# Create a Flask app
app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)
app.secret_key = 'your_secret_key'  

# Initialize the database
with app.app_context():
    init_db()

# Ensure the database connection is closed after each request
app.teardown_appcontext(close_connection)

# Import the routes
from routes.main_routes import main_bp
from routes.user_routes import user_bp

# Register the blueprints
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

