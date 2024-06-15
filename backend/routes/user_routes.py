from flask import Blueprint, request, jsonify
from utils.data_functions import get_next_events, update_elos, get_study_data

user_bp = Blueprint('user', __name__)

study_data = get_study_data()
# Change the number of questions here
number_of_questions = 4
# False will require users to choose the category and classfication
# True will only require users to select the better/worse event
omit_other = True

user_progress = {}
user_answers = {}
blacklist = []

@user_bp.route('/next', methods=['GET'])
def get_next():
    user_id = request.args.get('user_id')

    # No user ID provided
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    
    # User is blacklisted
    if user_id in blacklist:
        return jsonify({"message": "You are no longer a participant"}), 200
    
    # User has completed the study
    if user_id in user_progress and user_progress[user_id][0] >= number_of_questions:
        progress = {'current_completed': user_progress[user_id][0], 'number_of_questions': number_of_questions}
        return jsonify({"message": "Study completed", 'progress': progress}), 200
    
    # User has outstanding question (events to compare)
    if user_id in user_progress and user_progress[user_id][1] != []:
        progress = {'current_completed': user_progress[user_id][0], 'number_of_questions': number_of_questions}
        next_events_dict = {}
        next_events = [study_data.loc[study_data['event_ID'] == event_id] for event_id in user_progress[user_id][1]]
        for i, next_event in enumerate(next_events):
            next_events_dict[f"event{i}_details"] = str(next_event['event_details'].values[0])
            next_events_dict[f"event{i}_ID"] = int(next_event['event_ID'].values[0])
        return jsonify({'events': next_events_dict, 'progress': progress}), 200
    
    if user_id not in user_progress:
        user_progress[user_id] = [0, []]

    next_events = get_next_events(user_id, study_data)
    user_progress[user_id][1] = [int(next_events[f"event{i}_ID"]) for i in range(2)]
    progress = {'current_completed': user_progress[user_id][0], 'number_of_questions': number_of_questions}

    # Another check for study completion
    if not next_events:
        return jsonify({"message": "Study completed", 'progress': progress}), 200
    
    # Return the next events and the progress
    return jsonify({'events': next_events, 'progress': progress}), 200

@user_bp.route('/submit', methods=['POST'])
def submit_answer():
    user_id = request.json.get('user_id')

    # No user ID provided
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    
    # User ID not found
    if user_id not in user_progress:
        return jsonify({"error": "User ID not found"}), 400
    
    # User is blacklisted
    if user_id in blacklist:
        return jsonify({"message": "You are no longer a participant"}), 200
    
    # User has completed the study
    if user_id in user_progress and user_progress[user_id][0] >= number_of_questions:
        progress = {'current_completed': user_progress[user_id][0], 'number_of_questions': number_of_questions}
        return jsonify({"message": "Study completed", 'progress': progress}), 200
    
    loser_id = int(request.json.get('loser_id'))
    winner_id = int(request.json.get('winner_id'))
    polarity = request.json.get('polarization')
    
    # Polarity of the question not provided
    if not polarity:
        return jsonify({"error": "Polarity not provided"}), 400
    
    # Winner or loser ID not provided
    if not winner_id or not loser_id:
        return jsonify({"error": "Answer not provided"}), 400
    
    # Invalid winner or loser ID in the response (check against their assignment in user_progress)
    if winner_id not in user_progress[user_id][1] or loser_id not in user_progress[user_id][1]:
        return jsonify({"error": "Invalid answer"}), 400
    
    # Include the category and classification of the event/scenario
    if not omit_other:
        category = request.json.get('category')
        if not category:
            return jsonify({"error": "Category not provided"}), 400
        classification = request.json.get('classification')
        if not classification:
            return jsonify({"error": "Classification not provided"}), 400
        study_data.loc[study_data['event_ID'] == winner_id, category] += 1
        study_data.loc[study_data['event_ID'] == winner_id, classification] += 1
    
    update_elos(winner_id, loser_id, study_data)
    
    # Add the user's answer to the user_answers dictionary if it doesn't exist
    if user_id not in user_answers:
        user_answers[user_id] = []
    
    # Add the user's answer to the user_answers dictionary
    if not omit_other:
        user_answers[user_id].append([winner_id, loser_id, polarity, category, classification])
    else:
        user_answers[user_id].append([winner_id, loser_id, polarity])
    
    # Add one to the user's progress and clear the list of events to compare
    user_progress[user_id][0] += 1
    user_progress[user_id][1] = []

    progress = {'current_completed': user_progress[user_id][0], 'number_of_questions': number_of_questions}
    
    if user_progress[user_id][0] >= number_of_questions:
        return jsonify({"message": "Study completed", 'progress': progress}), 200

    next_events = get_next_events(user_id, study_data)
    user_progress[user_id][1] = [int(next_events[f"event{i}_ID"]) for i in range(2)]
    
    return jsonify({'events': next_events, 'progress': progress}), 200

@user_bp.route('/check_user_id', methods=['POST'])
def check_generated_user_id():
    user_id = request.json.get('user_id')
    
    # No user ID provided
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    
    # User ID already exists
    if user_id in user_progress:
        return jsonify({"message": "User ID already exists"}), 200
    
    return jsonify({"message": "User ID is valid", "questions_num": number_of_questions}), 200

@user_bp.route('/block_user', methods=['POST'])
def block_user():
    user_id = request.json.get('user_id')
    
    # No user ID provided
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    
    # Add the user to the blacklist
    blacklist.append(user_id)
    return jsonify({"message": "You are no longer a participant"}), 200