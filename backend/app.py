from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.data_functions import get_study_data, update_elos, get_next_events_based_on_elo

# For testing purposes
import random

# Create a Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'
number_of_questions = 2

# Load the study data as pandas DataFrame
study_data = get_study_data()

# For testing purposes print the columns
print(study_data.columns)

# Dictionary to keep track of users and their progress and current event_IDs for both events
# It is in the format {user_id: [(int) current_completed, [(int)event_ID1, (int)event_ID2]]}
user_progress = {}

# TODO:
# - Change route names
# - Maybe in the post also add requirement to add the loser ID for sanity check
# - Test limits
# - Change winner to loser (The users are asked to select the more negative event/experience)
# - Make sure there are no clashes with the selected events and also make that based on ELO rating

def get_next_events(user_id):
    if user_id not in user_progress:
        user_progress[user_id] = [0, []]

    # Check if the user has completed the study
    if user_progress[user_id][0] >= number_of_questions:
        return None

    # For now get 2 random even_details from study_data
    # Also right now you can get 2 same events
    next_events = get_next_events_based_on_elo(study_data)

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
        progress = {
            'current_completed': user_progress[user_id][0],
            'number_of_questions': number_of_questions,
        }
        
        return jsonify({"message": "Study completed", 'progress': progress}), 200


    # Check if the user has already got the next events assigned
    # If so continue with the same events as they have not been submitted yet
    if user_id in user_progress and user_progress[user_id][1] != []:
        progress = {
            'current_completed': user_progress[user_id][0],
            'number_of_questions': number_of_questions,
        }
        
        next_events_dict = {}
        next_events = [study_data.loc[study_data['event_ID'] == event_id] for event_id in user_progress[user_id][1]]
        
        for i, next_event in enumerate(next_events):
            next_events_dict[f"event{i}_details"] = str(next_event['event_details'].values[0])
            next_events_dict[f"event{i}_ID"] = int(next_event['event_ID'].values[0])

        return jsonify({'events': next_events_dict, 'progress': progress}), 200

    # Get the next questions
    # If the next questions are empty, the user has completed the study
    next_events = get_next_events(user_id)

    progress = {
        'current_completed': user_progress[user_id][0],
        'number_of_questions': number_of_questions,
    }

    # If the next questions are empty, the user has completed the study
    if not next_events:
        return jsonify({"message": "Study completed", 'progress': progress}), 200
    
    # Also include the number of questions the user has answered
    return jsonify({'events': next_events, 'progress': progress}), 200


@app.route('/submit', methods=['POST'])
def submit_answer():
    # The user ID is handled on the frontend
    user_id = request.json.get('user_id')

    # Check if the user ID is provided
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400

    if user_id not in user_progress:
        return jsonify({"error": "User ID not found"}), 400
    
    # Check if the user has completed the study
    # In this function it is in two places to avoid any issues when checking for winner_id
    if user_id in user_progress and user_progress[user_id][0] >= number_of_questions:
        progress = {
            'current_completed': user_progress[user_id][0],
            'number_of_questions': number_of_questions,
        }

        return jsonify({"message": "Study completed", 'progress': progress}), 200
    
    # winner is actuallu a loser since the users are selecting the more negative event/experiencce
    winner_id = int(request.json.get('winner_id'))
    if not winner_id:
        return jsonify({"error": "Answer not provided"}), 400
    
    loser_id = int(user_progress[user_id][1][0]) if int(user_progress[user_id][1][0]) != winner_id else int(user_progress[user_id][1][1])

    category = request.json.get('category')
    if not category:
        return jsonify({"error": "Category not provided"}), 400
    
    classification = request.json.get('classification')
    if not classification:
        return jsonify({"error": "Classification not provided"}), 400

    # Make sure the winner ID and loser ID are the sane as the assigned event IDs
    if winner_id not in user_progress[user_id][1]:
        print(f"Received answer from {user_id}: {winner_id}, {loser_id}")
        print(f"Assigned events: {user_progress[user_id][1]}")
        return jsonify({"error": "Invalid answer"}), 400

    # Update the user progress
    user_progress[user_id][0] += 1
    user_progress[user_id][1] = []

    # Include the progress in the response
    # This will help users track their progress, it is used in the prorgess bar in the frontend
    progress = {
        'current_completed': user_progress[user_id][0],
        'number_of_questions': number_of_questions,
    }

    # Get the ELO ratings of the winner and loser
    winner_elo = study_data.loc[study_data['event_ID'] == winner_id, 'elo_rating']
    loser_elo = study_data.loc[study_data['event_ID'] == loser_id, 'elo_rating']

    # Get updated ELO ratings
    winner_new_elo, loser_new_elo = update_elos(winner_elo.values[0], loser_elo.values[0])

    # Print the changes (event_IDs and ELO ratings new and old)
    # Only for testing purposes  
    print(f"Winner: {winner_id}, Old ELO: {winner_elo.values[0]}, New ELO: {winner_new_elo}")
    print(f"Loser: {loser_id}, Old ELO: {loser_elo.values[0]}, New ELO: {loser_new_elo}")

    # Update the ELO ratings in the study data
    study_data.loc[study_data['event_ID'] == winner_id, 'elo_rating'] = winner_new_elo
    study_data.loc[study_data['event_ID'] == loser_id, 'elo_rating'] = loser_new_elo

    # Update the category and classification counters
    study_data.loc[study_data['event_ID'] == winner_id, category] += 1
    study_data.loc[study_data['event_ID'] == winner_id, classification] += 1

    # For testing purposes print all the categories and classifications
    # print(study_data.loc[study_data['event_ID'] == winner_id, ['Health', 'Financial', 'Relationship', 'Bereavement', 'Work', 'Crime', 'Daily', 'Major']])

    # Get the next set of events
    next_events = get_next_events(user_id)

    # If the next questions are empty, the user has completed the study
    if not next_events:
        return jsonify({"message": "Study completed", 'progress': progress}), 200

    # Also include the number of questions the user has answered
    return jsonify({'events': next_events, 'progress': progress}), 200

# Used to check if the generated UUID is valid
# As with everything this needs to be changed if concurency is going to be used
@app.route('/check_user_id', methods=['POST'])
def check_generated_user_id():
    user_id = request.json.get('user_id')

    if user_id in user_progress:
        return jsonify({"message": "User ID already exists"}), 200

    # Also include the number of questions the user has to answer
    return jsonify({"message": "User ID is valid"}), 200

@app.route('/', methods=['GET'])
def home():
    user_id = request.args.get('user_id')
    with app.test_request_context('/next', method='GET', query_string={'user_id': user_id}):
        return get_next()

if __name__ == '__main__':
    app.run(debug=True)
