from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.data_functions import get_study_data, update_elos

# For testing purposes
import random

# Create a Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'
number_of_questions = 2

# Load the study data as pandas DataFrame
study_data = get_study_data()

# Dictionary to keep track of users and their progress and current event_IDs for both events
user_progress = {}

# TODO:
# - Change route names
# - Add next events be probabilistic based on ELO ratings
# - Maybe in the post also add requirement to add the loser ID for sanity check
# - Test limits

# Returns list of 2 DataFrame rows with event details
def get_next_events_based_on_elo():
    next_events = [study_data.loc[study_data['event_ID'] == random.randint(1, len(study_data))] for _ in range(2)]
    return next_events

def get_next_events(user_id):
    if user_id not in user_progress:
        user_progress[user_id] = [0, []]

    current_completed = user_progress[user_id][0]

    # Check if the user has completed all the questions
    if current_completed >= number_of_questions:
        return {}

    # For now get 2 random even_details from study_data
    # Also right now you can get 2 same events
    next_events = get_next_events_based_on_elo()

    # Set curret events for the user using int(event_ID)s
    user_progress[user_id][1] = [int(next_event['event_ID'].values[0]) for next_event in next_events]

    next_events_dict = {}
    for i, next_event in enumerate(next_events):
        next_events_dict[f"event{i}_details"] = str(next_event['event_details'].values[0])
        next_events_dict[f"event{i}_ID"] = int(next_event['event_ID'].values[0])

    return next_events_dict

# this route gets the next question for the user
@app.route('/next', methods=['GET'])
def get_next():
    # The user ID is handled on the frontend
    user_id = request.args.get('user_id')

    # Check if the user ID is provided
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    
    # Check if the user has completed the study
    if user_id in user_progress and user_progress[user_id][0] >= number_of_questions:
        return jsonify({"message": "Study completed"}), 200

    # Check if the user has already got the next events assigned
    # If so continue with the same events as they have not been submitted yet
    if user_id in user_progress and user_progress[user_id][1] != []:
        next_events_dict = {}
        next_events = [study_data.loc[study_data['event_ID'] == event_id] for event_id in user_progress[user_id][1]]
        
        for i, next_event in enumerate(next_events):
            next_events_dict[f"event{i}_details"] = str(next_event['event_details'].values[0])
            next_events_dict[f"event{i}_ID"] = int(next_event['event_ID'].values[0])

        return jsonify({'events': next_events_dict}), 200

    # Get the next questions
    # If the next questions are empty, the user has completed the study
    next_events = get_next_events(user_id)

    # If the next questions are empty, the user has completed the study
    if not next_events:
        return jsonify({"message": "Study completed"}), 200
    
    return jsonify({'events': next_events}), 200


@app.route('/submit', methods=['POST'])
def submit_answer():
    # The user ID is handled on the frontend
    user_id = request.json.get('user_id')

    # Check if the user ID is provided
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400

    if user_id not in user_progress:
        return jsonify({"error": "User ID not found"}), 400
    
    winner_id = int(request.json.get('winner_id'))
    if not winner_id:
        return jsonify({"error": "Answer not provided"}), 400
    print(user_progress[user_id][1], winner_id)
    loser_id = int(user_progress[user_id][1][0]) if int(user_progress[user_id][1][0]) != winner_id else int(user_progress[user_id][1][1])

    # Make sure the winner ID and loser ID are the sane as the assigned event IDs
    if winner_id not in user_progress[user_id][1]:
        print(f"Received answer from {user_id}: {winner_id}, {loser_id}")
        print(f"Assigned events: {user_progress[user_id][1]}")
        return jsonify({"error": "Invalid answer"}), 400

    # Handle the submitted answer here
    print(f"Received answer from {user_id}: {winner_id}")

    # Update the user progress
    user_progress[user_id][0] += 1
    user_progress[user_id][1] = []

    # Get the ELO ratings of the winner and loser
    # Make sure to convert the ELO ratings to integers from pandas float64
    winner_elo = study_data.loc[study_data['event_ID'] == winner_id, 'elo_rating']
    loser_elo = study_data.loc[study_data['event_ID'] == loser_id, 'elo_rating']

    # Get updated ELO ratings
    winner_new_elo, loser_new_elo = update_elos(winner_elo.values[0], loser_elo.values[0])

    # Print the changes (event_IDs and ELO ratings new and old)
    print(f"Winner: {winner_id}, Old ELO: {winner_elo.values[0]}, New ELO: {winner_new_elo}")
    print(f"Loser: {loser_id}, Old ELO: {loser_elo.values[0]}, New ELO: {loser_new_elo}")

    # Update the ELO ratings in the study data
    study_data.loc[study_data['event_ID'] == winner_id, 'elo_rating'] = winner_new_elo
    study_data.loc[study_data['event_ID'] == loser_id, 'elo_rating'] = loser_new_elo

    # Get the next set of events
    next_events = get_next_events(user_id)

    # If the next questions are empty, the user has completed the study
    if not next_events:
        return jsonify({"message": "Study completed"}), 200

    return jsonify({'events': next_events}), 200

@app.route('/', methods=['GET'])
def home():
    user_id = request.args.get('user_id')
    with app.test_request_context('/next', method='GET', query_string={'user_id': user_id}):
        return get_next()

if __name__ == '__main__':
    app.run(debug=True)
