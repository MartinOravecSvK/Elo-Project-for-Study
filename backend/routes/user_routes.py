from flask import Flask, Blueprint, request, jsonify
from flask_apscheduler import APScheduler
from flask_apscheduler import APScheduler
from utils.data_functions import get_next_events, update_elos, get_study_data, get_next_events_test
import time
import json

from data.global_data import user_progress, user_answers, blacklist, number_of_questions, omit_other, study_data
from locks.locks import user_progress_lock, user_answers_lock, blacklist_lock, study_data_lock

import random
generate_random_user_id = lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))


user_bp = Blueprint('user', __name__)

# Sheduler to save data 
# ______________________________________________________________________________________________________________________

app = Flask(__name__)
scheduler = APScheduler()

user_bp = Blueprint('user', __name__)

def save_data():
    user_answers_file = 'output/user_answers.json'
    with user_answers_lock:
        with open(user_answers_file, 'w') as f:
            json.dump(user_answers, f)

    study_data_file = 'output/study_data.csv'
    with study_data_lock:
        study_data.to_csv(study_data_file)

scheduler.add_job(id='Save Data', func=save_data, trigger='interval', seconds=10) 

def start_scheduler():
    print('Starting scheduler')
    if not scheduler.running:
        scheduler.start()

def shutdown_scheduler():
    print('Shutting down scheduler')
    if scheduler.running:
        scheduler.shutdown(wait=False)
# ______________________________________________________________________________________________________________________

@user_bp.route('/next', methods=['GET'])
def get_next():
    user_id = request.args.get('user_id')

    # No user ID provided
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    
    with blacklist_lock:
        # User is blacklisted
        if user_id in blacklist:
            return jsonify({"message": "You are no longer a participant"}), 200
    
    with user_progress_lock:
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
                # next_events_dict[f"event{i}_details"] = str(next_event['event_details'].values[0])
                next_events_dict[f"event{i}_details"] = str(next_event['event_CLEANED'].values[0])
                next_events_dict[f"event{i}_ID"] = int(next_event['event_ID'].values[0])
            return jsonify({'events': next_events_dict, 'progress': progress}), 200
        
        if user_id not in user_progress:
            user_progress[user_id] = [0, [], time.time()]

    with study_data_lock:
        # next_events = get_next_events_test(study_data)
        next_events = get_next_events(study_data)
    with user_progress_lock:
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
    
    with user_progress_lock:
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
    
    with user_progress_lock:
        # Invalid winner or loser ID in the response (check against their assignment in user_progress)
        if winner_id not in user_progress[user_id][1] or loser_id not in user_progress[user_id][1]:
            return jsonify({"error": "Invalid answer"}), 400
        
        delta_time = time.time() - user_progress[user_id][2]
    
    # Include the category and classification of the event/scenario
    if not omit_other:
        category = request.json.get('category')
        if not category:
            return jsonify({"error": "Category not provided"}), 400
        classification = request.json.get('classification')
        if not classification:
            return jsonify({"error": "Classification not provided"}), 400
        with study_data_lock:
            study_data.loc[study_data['event_ID'] == winner_id, category] += 1
            study_data.loc[study_data['event_ID'] == winner_id, classification] += 1
    
    with study_data_lock:
        update_elos(winner_id, loser_id, study_data)
    
    with user_answers_lock:
        # Add the user's answer to the user_answers dictionary if it doesn't exist
        if user_id not in user_answers:
            user_answers[user_id] = []
    
        # Add the user's answer to the user_answers dictionary
        if not omit_other:
            user_answers[user_id].append([winner_id, loser_id, polarity, category, classification, delta_time])
        else:
            user_answers[user_id].append([winner_id, loser_id, polarity, delta_time])
    
    with user_progress_lock:
        # Add one to the user's progress and clear the list of events to compare
        user_progress[user_id][0] += 1
        user_progress[user_id][1] = []

    progress = {'current_completed': user_progress[user_id][0], 'number_of_questions': number_of_questions}
    
    if user_progress[user_id][0] >= number_of_questions:
        return jsonify({"message": "Study completed", 'progress': progress}), 200

    with study_data_lock:
        # next_events = get_next_events_test(study_data)
        next_events = get_next_events(study_data)
    with user_progress_lock:
        user_progress[user_id][1] = [int(next_events[f"event{i}_ID"]) for i in range(2)]
        user_progress[user_id][2] = time.time()
    
    return jsonify({'events': next_events, 'progress': progress}), 200

@user_bp.route('/check_user_id', methods=['POST'])
def check_generated_user_id():
    user_id = request.json.get('user_id')
    
    # No user ID provided
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    
    with user_progress_lock:
        # User ID already exists
        if user_id in user_progress:
            return jsonify({"message": "User ID already exists"}), 200
        
    with user_answers_lock:
        # User ID already exists
        if user_id in user_answers:
            return jsonify({"message": "User ID already exists"}), 200
    
    return jsonify({"message": "User ID is valid", "questions_num": number_of_questions}), 200

@user_bp.route('/generate_user_id', methods=['POST'])
def generate_user_id():
    # Generate a random user ID with 9 random characters
    user_id = generate_random_user_id()
    with user_progress_lock:
        while user_id in user_progress:
            user_id = generate_random_user_id()
        # Add the user ID to the user_progress dictionary
        user_progress[user_id] = [0, [], time.time()]

    return jsonify({"user_id": user_id, "questions_num": number_of_questions}), 200

@user_bp.route('/block_user', methods=['POST'])
def block_user():
    user_id = request.json.get('user_id')
    
    # No user ID provided
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    
    with blacklist_lock:
        # Add the user to the blacklist
        blacklist.append(user_id)

    return jsonify({"message": "You are no longer a participant"}), 200
