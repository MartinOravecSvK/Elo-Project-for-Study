from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.data_functions import get_study_data 

# For testing purposes
import random

# Create a Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'

# Load the study data as pandas DataFrame
study_data = get_study_data()

# Dictionary to keep track of users and their progress and current event_IDs for both events
user_progress = {}

def get_next_events(user_id):
    if user_id not in user_progress:
        user_progress[user_id] = 0

    current_completed = user_progress[user_id]

    # Check if the user has completed all the questions
    if current_completed >= len(study_data):
        # Handle the completion of the study using empty list as flag
        return []

    # For now get 2 random even_details from study_data
    next_events = []
    for i in range(2):
        # Get the next event
        # For now, just get a random event
        rand_id = random.randint(0, len(study_data) - 1)
        next_event = study_data.iloc[rand_id]
        next_events.append({
            f"event{i}_details": next_event['event_details'],
            f"event{i}_ID": next_event['event_ID']
        })

    return next_events

@app.route('/next', methods=['GET'])
def get_next_question():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    
    # Get the next questions
    # If the next questions are empty, the user has completed the study
    next_events = get_next_events(user_id)

    if next_events == []:
        return jsonify({"message": "Study completed"}), 200
    
    return jsonify(next_events), 200

@app.route('/submit', methods=['POST'])
def submit_answer():
    # Get the user ID from the request
    user_id = request.json.get('user_id')

    # Check if the user ID is provided
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400

    data = request.json.get('answer')
    if not data:
        return jsonify({"error": "Answer not provided"}), 400

    # Handle the submitted answer here
    print(f"Received answer from {user_id}: {data}")

    # Update the user progress and ELO ratings


    # Get the next questions
    next_events = get_next_events(user_id)

    return jsonify(next_events), 200

if __name__ == '__main__':
    app.run(debug=True)
