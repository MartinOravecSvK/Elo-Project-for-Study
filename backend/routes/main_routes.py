import os
from flask import Blueprint, send_from_directory, current_app

main_bp = Blueprint('main', __name__)

@main_bp.route('/kimberley/Elo-Study/backend/')
def backend_index():
    return send_from_directory(current_app.static_folder, 'index.html')

@main_bp.route('/kimberley/Elo-Study/backend/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(current_app.static_folder, path)):
        return send_from_directory(current_app.static_folder, path)