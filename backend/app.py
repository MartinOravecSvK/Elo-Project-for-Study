import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
from flask_cors import CORS
import atexit

# Create a Flask app
app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)
app.secret_key = 'your_secret_key'  

# Import the routes
from routes.main_routes import main_bp
from routes.user_routes import user_bp, configure_scheduler, shutdown_scheduler

# Register the blueprints
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)

# Configure and start the scheduler
configure_scheduler(app)

# Register shutdown function for when the app exits
atexit.register(lambda: shutdown_scheduler())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

