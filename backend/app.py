import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
from flask_cors import CORS

# Create a Flask app
app = Flask(__name__, static_folder='../frontend/build', static_url_path='/kimberley/Elo-Study/backend')
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow requests from your frontend dev server
app.secret_key = 'your_secret_key'

# Import the routes
from routes.main_routes import main_bp
from routes.user_routes import user_bp, scheduler

# Register the blueprints
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)

@app.before_first_request
def start_scheduler():
    scheduler.init_app(app)
    scheduler.start()

@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    scheduler.shutdown()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

# WSGI entry point
application = app

# from flask import Flask

# app = Flask(__name__, static_folder='../build', static_url_path='/')

# from routes.main_routes import main_bp
# from routes.user_routes import user_bp

# app.register_blueprint(main_bp)
# app.register_blueprint(user_bp)

# if __name__ == '__main__':
#     app.run
