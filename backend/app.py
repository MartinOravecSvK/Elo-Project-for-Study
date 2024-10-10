import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
from flask_cors import CORS
import atexit

# Create a Flask app
app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)
app.secret_key = 'your_secret_key'  

# Import the routes
from routes.main_routes import main_bp
from routes.user_routes import user_bp, scheduler, start_scheduler, shutdown_scheduler

# Register the blueprints
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)

# Register a function to run before the first request
@app.before_request
def before_request():
    if not hasattr(app, 'scheduler_started'):
        start_scheduler()
        app.scheduler_started = True

atexit.register(lambda: scheduler.shutdown(wait=False))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

