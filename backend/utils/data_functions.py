from pandas import read_excel, read_csv
import pandas as pd
from os import path
import random
import numpy as np
import json

# Columns to drop from the study data                          
# 'event_valence' might be useful for better ELO rating calculation
DROP_COLUMNS = ['fileName', 'study_number', 'participant_ID', 'event_valence', 'event_when', 'event_known', 'Use?', 'event_details']

# Additional columns for the study data (all just counters)
categories = ['Health', 'Financial', 'Relationship', 'Bereavement', 'Work', 'Crime']
classification = ['Daily', 'Major']

# Returns the study data as a pandas DataFrame
# Columns: ['event_details', 'event_ID', 'elo_rating']
def get_study_data():
    study_data_file = 'output/study_data.json'
    if path.exists(study_data_file):
        study_data = pd.read_json(study_data_file, orient='split')
    else:
        # Get the study data path
        current_dir = path.dirname(path.abspath(__file__))
        study_data_path = path.join(current_dir, '../data/All_Studies_SigEvent_details_CLEANED_23.05.2024.xlsx')

        # Load the study data
        study_data = read_excel(study_data_path, engine='openpyxl')

        # Use only rows with Use? set to Yes
        study_data = study_data[study_data['Use?'] == 'Yes']

        # Drop the unnecessary columns
        study_data.drop(columns=DROP_COLUMNS, inplace=True)

        # Initialize ELO rating for each sentence based on the slider_end column ((doesn't make sense)0 - (makes complete sense)100)
        slider_factor = 2.5
        initial_elo = ((1000 - 50 * slider_factor) + study_data['slider_end'] * slider_factor).astype(int)
        study_data['elo_rating'] = initial_elo

        # Add a column to keep track of the number of times the event has been seen
        # Since, ideally, all events should be seen the same number of times
        study_data['seen'] = 0

        # Add instability column [+/-]
        study_data['instability'] = 0

        # Drop the slider_end column
        study_data.drop(columns=['slider_end'], inplace=True)

        # Finally add additional columns for the study data
        study_data['Health'] = 0
        study_data['Financial'] = 0
        study_data['Relationship'] = 0
        study_data['Bereavement'] = 0
        study_data['Work'] = 0
        study_data['Crime'] = 0
        study_data['Daily'] = 0
        study_data['Major'] = 0
    
    return study_data

def get_historical_data(study_data):
    elo_history_file = 'output/elo_history.json'
    if path.exists(elo_history_file):
        with open(elo_history_file, 'r') as f:
            elo_history = json.load(f)
    else:
        elo_history = {}

    # Initialize ELO history for each event if needed
    if elo_history == {}:
        for index, row in study_data.iterrows():
            event_id = row['event_ID']
            if event_id not in elo_history:
                elo_history[str(event_id)] = [row['elo_rating']]

    return elo_history

# Gets the saved user progress or initializes it
def get_user_answers():
    user_answers_file = 'output/user_answers.json'
    try:
        with open(user_answers_file, 'r') as f:
            user_answers = json.load(f)
    except FileNotFoundError:
        user_answers = {}

    return user_answers

def update_elos(db, winner_id, loser_id):
    c = db.cursor()
    # Get current ELO ratings
    c.execute('SELECT elo_rating FROM study_data WHERE event_ID = ?', (winner_id,))
    winner_elo = c.fetchone()[0]
    c.execute('SELECT elo_rating FROM study_data WHERE event_ID = ?', (loser_id,))
    loser_elo = c.fetchone()[0]

    # Constants for ELO rating calculation
    K = 32

    # Calculate expected scores
    expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    expected_loser = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))

    # Calculate new ELO ratings
    winner_new_elo = winner_elo + int(K * (1 - expected_winner))
    loser_new_elo = loser_elo + int(K * (0 - expected_loser))

    # Update ELO ratings in study_data
    c.execute('UPDATE study_data SET elo_rating = ? WHERE event_ID = ?', (winner_new_elo, winner_id))
    c.execute('UPDATE study_data SET elo_rating = ? WHERE event_ID = ?', (loser_new_elo, loser_id))

    # Update elo_history
    c.execute('SELECT history FROM elo_history WHERE event_ID = ?', (winner_id,))
    winner_history = c.fetchone()
    if winner_history:
        winner_history = json.loads(winner_history[0])
    else:
        winner_history = []
    winner_history.append(winner_new_elo)
    c.execute('''
        INSERT OR REPLACE INTO elo_history (event_ID, history)
        VALUES (?, ?)
    ''', (winner_id, json.dumps(winner_history)))

    c.execute('SELECT history FROM elo_history WHERE event_ID = ?', (loser_id,))
    loser_history = c.fetchone()
    if loser_history:
        loser_history = json.loads(loser_history[0])
    else:
        loser_history = []
    loser_history.append(loser_new_elo)
    c.execute('''
        INSERT OR REPLACE INTO elo_history (event_ID, history)
        VALUES (?, ?)
    ''', (loser_id, json.dumps(loser_history)))


def get_next_events(db, user_id):
    c = db.cursor()
    # Get user answers to exclude seen events
    c.execute('SELECT winner_id, loser_id FROM user_answers WHERE user_id = ?', (user_id,))
    user_answers = c.fetchall()
    seen_event_ids = set()
    for winner_id, loser_id in user_answers:
        seen_event_ids.update([winner_id, loser_id])

    # Retrieve eligible events
    query = '''
        SELECT event_ID, event_CLEANED, elo_rating, seen
        FROM study_data
        WHERE event_ID NOT IN ({})
    '''.format(','.join('?' * len(seen_event_ids)) if seen_event_ids else '0')
    c.execute(query, tuple(seen_event_ids))

    events = c.fetchall()
    if len(events) < 2:
        return None  # Not enough events to compare

    # Sort events by elo_rating
    events.sort(key=lambda x: x[2])  # x[2] is elo_rating

    # Implement your logic to select two events
    # For simplicity, select two events with closest elo_rating
    index = random.randint(0, len(events) - 2)
    event1 = events[index]
    event2 = events[index + 1]

    # Update 'seen' count
    c.execute('UPDATE study_data SET seen = seen + 1 WHERE event_ID = ?', (event1[0],))
    c.execute('UPDATE study_data SET seen = seen + 1 WHERE event_ID = ?', (event2[0],))
    db.commit()

    next_events = {
        'event0_details': event1[1],
        'event0_ID': event1[0],
        'event1_details': event2[1],
        'event1_ID': event2[0]
    }
    return next_events



# Returns list of 2 DataFrame rows with event details
def get_next_events_based_on_elo(study_data, window_size=10, exclude_event_ids=None):
    if exclude_event_ids is None:
        exclude_event_ids = set()

    # First sort the data by elo_rating
    sorted_data = study_data.sort_values(by='elo_rating').reset_index(drop=True)

    # Exclude events that are in exclude_event_ids
    eligible_events = sorted_data[~sorted_data['event_ID'].isin(exclude_event_ids)].reset_index(drop=True)

    # Ensure the events are not repeated and their 'seen' counts are balanced
    eligible_events = eligible_events[eligible_events['seen'] < eligible_events['seen'].mean() + 1]

    # If not enough eligible events, fallback to any events not in exclude_event_ids
    if len(eligible_events) < 2:
        eligible_events = sorted_data[~sorted_data['event_ID'].isin(exclude_event_ids)].reset_index(drop=True)

    # If still not enough, fallback to any events
    if len(eligible_events) < 2:
        eligible_events = sorted_data.reset_index(drop=True)

    # Randomly select the first event
    index1 = random.randint(0, len(eligible_events) - 1)

    # Define the range for the second event selection
    lower_bound = max(0, index1 - window_size)
    upper_bound = min(len(eligible_events) - 1, index1 + window_size)

    # Generate a range of indices around the first event
    indices = np.arange(lower_bound, upper_bound + 1)

    # Calculate probabilities using Gaussian PDF centered at index1
    mean = index1
    sigma = window_size / 2  # Standard deviation can be adjusted
    probabilities = np.exp(-0.5 * ((indices - mean) / sigma) ** 2)
    probabilities /= probabilities.sum()  # Normalize to sum to 1

    # Select the second event probabilistically
    # Ensure index2 is not the same as index1
    index2 = np.random.choice(indices, p=probabilities)
    while index1 == index2:
        index2 = np.random.choice(indices, p=probabilities)

    event1 = eligible_events.iloc[index1]
    event2 = eligible_events.iloc[index2]

    return [event1, event2]


if __name__ == '__main__':
    # Load the study data
    study_data = get_study_data()

    # Print the study data columns
    print(study_data.columns)
    print(study_data.head())

    # Print the longest event_details
    print('Longest event_details: ', study_data['event_details'].apply(lambda x: len(str(x))).max())
    # Also print the event_ID of the longest event_details
    print('Longest event_details ID: ', study_data.loc[study_data['event_details'].apply(lambda x: len(str(x))) == study_data['event_details'].apply(lambda x: len(str(x))).max(), 'event_ID'].values[0])

    # Print the average event_details
    print('Mean event_details: ', study_data['event_details'].apply(lambda x: len(str(x))).mean())