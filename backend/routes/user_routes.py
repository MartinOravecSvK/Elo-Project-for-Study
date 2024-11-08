from flask import Blueprint, request, jsonify
from utils.data_functions import get_next_events, update_elos, get_study_data
import time
import json
import pandas as pd
from db import get_db

from data.global_data import number_of_questions, omit_other

import random
generate_random_user_id = lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))

user_bp = Blueprint('user', __name__)

import pandas as pd
import json

def save_data():
    db = get_db()
    c = db.cursor()

    # Save user_answers
    c.execute('SELECT * FROM user_answers')
    user_answers_rows = c.fetchall()
    user_answers_columns = [description[0] for description in c.description]
    user_answers_df = pd.DataFrame(user_answers_rows, columns=user_answers_columns)
    user_answers_file = 'output/user_answers.json'
    user_answers_df.to_json(user_answers_file, orient='records', indent=4)

    # Save study_data
    c.execute('SELECT * FROM study_data')
    study_data_rows = c.fetchall()
    study_data_columns = [description[0] for description in c.description]
    study_data_df = pd.DataFrame(study_data_rows, columns=study_data_columns)
    study_data_file = 'output/study_data.json'
    study_data_df.to_json(study_data_file, orient='split', default_handler=str)

    # Save elo_history
    c.execute('SELECT event_ID, history FROM elo_history')
    elo_history_rows = c.fetchall()
    elo_history_dict = {}
    for event_ID, history_json in elo_history_rows:
        elo_history_dict[str(event_ID)] = json.loads(history_json)
    elo_history_file = 'output/elo_history.json'
    with open(elo_history_file, 'w') as f:
        json.dump(elo_history_dict, f, indent=4)



def get_events_details(event_ids):
    db = get_db()
    c = db.cursor()
    placeholders = ', '.join('?' for _ in event_ids)
    query = f'''
        SELECT event_ID, event_CLEANED
        FROM study_data
        WHERE event_ID IN ({placeholders})
    '''
    c.execute(query, event_ids)
    events = c.fetchall()
    events_dict = {}
    for i, (event_ID, event_CLEANED) in enumerate(events):
        events_dict[f"event{i}_details"] = event_CLEANED
        events_dict[f"event{i}_ID"] = event_ID
    return events_dict


@user_bp.route('/next', methods=['GET'])
def get_next():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400

    db = get_db()
    c = db.cursor()

    # Check if user is blacklisted
    c.execute('SELECT 1 FROM blacklist WHERE user_id = ?', (user_id,))
    if c.fetchone():
        return jsonify({"message": "You are no longer a participant"}), 200

    # Get user progress
    c.execute('''
        SELECT progress, event1_id, event2_id
        FROM user_progress
        WHERE user_id = ?
    ''', (user_id,))
    user_row = c.fetchone()

    if user_row:
        progress, event1_id, event2_id = user_row
        # Check if user has completed the study
        if progress >= number_of_questions:
            progress_info = {'current_completed': progress, 'number_of_questions': number_of_questions}
            save_data()
            print("progress >= number_of_questions")
            return jsonify({"message": "Study completed", 'progress': progress_info}), 200

        # If user has outstanding events
        if event1_id and event2_id:
            progress_info = {'current_completed': progress, 'number_of_questions': number_of_questions}
            events = get_events_details([event1_id, event2_id])
            return jsonify({'events': events, 'progress': progress_info}), 200
    else:
        # Create new user progress
        timestamp = time.time()
        c.execute('''
            INSERT INTO user_progress (user_id, progress, timestamp)
            VALUES (?, ?, ?)
        ''', (user_id, 0, timestamp))
        db.commit()

    # Generate next events
    next_events = get_next_events(db, user_id)
    if not next_events:
        progress_info = {'current_completed': 0, 'number_of_questions': number_of_questions}
        save_data()
        print("not next_events")
        return jsonify({"message": "Study completed", 'progress': progress_info}), 200

    event1_id, event2_id = next_events['event0_ID'], next_events['event1_ID']
    # Update user_progress with new events
    c.execute('''
        UPDATE user_progress
        SET event1_id = ?, event2_id = ?, timestamp = ?
        WHERE user_id = ?
    ''', (event1_id, event2_id, time.time(), user_id))
    db.commit()

    progress_info = {'current_completed': 0, 'number_of_questions': number_of_questions}
    return jsonify({'events': next_events, 'progress': progress_info}), 200

@user_bp.route('/submit', methods=['POST'])
def submit_answer():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400

    db = get_db()
    c = db.cursor()

    # Check if user exists
    c.execute('''
        SELECT progress, event1_id, event2_id, timestamp
        FROM user_progress
        WHERE user_id = ?
    ''', (user_id,))
    user_row = c.fetchone()
    if not user_row:
        return jsonify({"error": "User ID not found"}), 400

    progress, event1_id, event2_id, timestamp = user_row

    # Check if user is blacklisted
    c.execute('SELECT 1 FROM blacklist WHERE user_id = ?', (user_id,))
    if c.fetchone():
        return jsonify({"message": "You are no longer a participant"}), 200

    # Check if user has completed the study
    if progress >= number_of_questions:
        progress_info = {'current_completed': progress, 'number_of_questions': number_of_questions}
        save_data()
        return jsonify({"message": "Study completed", 'progress': progress_info}), 200

    # Get submitted data
    loser_id = int(request.json.get('loser_id'))
    winner_id = int(request.json.get('winner_id'))
    polarity = request.json.get('polarization')
    if not polarity:
        return jsonify({"error": "Polarity not provided"}), 400

    # Validate winner and loser IDs
    if winner_id not in [event1_id, event2_id] or loser_id not in [event1_id, event2_id]:
        return jsonify({"error": "Invalid answer"}), 400

    delta_time = time.time() - timestamp

    # Update study_data and elo_history
    update_elos(db, winner_id, loser_id)

    # Insert into user_answers
    if not omit_other:
        category = request.json.get('category')
        classification = request.json.get('classification')
        if not category or not classification:
            return jsonify({"error": "Category or Classification not provided"}), 400

        c.execute('''
            INSERT INTO user_answers (user_id, winner_id, loser_id, polarity, category, classification, delta_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, winner_id, loser_id, polarity, category, classification, delta_time))

        # Update category and classification counts
        c.execute(f'''
            UPDATE study_data
            SET {category} = {category} + 1, {classification} = {classification} + 1
            WHERE event_ID = ?
        ''', (winner_id,))
    else:
        c.execute('''
            INSERT INTO user_answers (user_id, winner_id, loser_id, polarity, delta_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, winner_id, loser_id, polarity, delta_time))

    # Update user progress
    progress += 1
    c.execute('''
        UPDATE user_progress
        SET progress = ?, event1_id = NULL, event2_id = NULL, timestamp = ?
        WHERE user_id = ?
    ''', (progress, time.time(), user_id))

    db.commit()

    progress_info = {'current_completed': progress, 'number_of_questions': number_of_questions}
    if progress >= number_of_questions:
        save_data()
        return jsonify({"message": "Study completed", 'progress': progress_info}), 200

    # Generate next events
    next_events = get_next_events(db, user_id)
    if not next_events:
        save_data()
        return jsonify({"message": "Study completed", 'progress': progress_info}), 200

    event1_id, event2_id = next_events['event0_ID'], next_events['event1_ID']
    # Update user_progress with new events
    c.execute('''
        UPDATE user_progress
        SET event1_id = ?, event2_id = ?, timestamp = ?
        WHERE user_id = ?
    ''', (event1_id, event2_id, time.time(), user_id))
    db.commit()

    return jsonify({'events': next_events, 'progress': progress_info}), 200

@user_bp.route('/check_user_id', methods=['POST'])
def check_generated_user_id():
    user_id = request.json.get('user_id')
    
    # No user ID provided
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400

    db = get_db()
    c = db.cursor()

    # Check if user ID exists in user_progress
    c.execute('SELECT 1 FROM user_progress WHERE user_id = ?', (user_id,))
    if c.fetchone():
        return jsonify({"message": "User ID already exists"}), 200

    # Check if user ID exists in user_answers
    c.execute('SELECT 1 FROM user_answers WHERE user_id = ?', (user_id,))
    if c.fetchone():
        return jsonify({"message": "User ID already exists"}), 200

    return jsonify({"message": "User ID is valid", "questions_num": number_of_questions}), 200

@user_bp.route('/block_user', methods=['POST'])
def block_user():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400

    db = get_db()
    c = db.cursor()

    # Add user to blacklist
    c.execute('INSERT OR IGNORE INTO blacklist (user_id) VALUES (?)', (user_id,))
    db.commit()

    return jsonify({"message": "You are no longer a participant"}), 200

