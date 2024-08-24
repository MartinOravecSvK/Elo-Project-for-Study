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
    study_data_file = 'output/study_data.csv'
    # try:
        # study_data = read_csv(study_data_file)
    if path.exists(study_data_file):
        study_data = pd.read_json(study_data_file, orient='split')
    # except FileNotFoundError:
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
    for index, row in study_data.iterrows():
        event_id = row['event_ID']
        if event_id not in elo_history:
            elo_history[event_id] = [row['elo_rating']]

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

def update_elos(winner_id, loser_id, study_data, elo_history):
    # Get current ELO ratings
    winner_elo = study_data.loc[study_data['event_ID'] == winner_id, 'elo_rating'].iloc[0]
    loser_elo = study_data.loc[study_data['event_ID'] == loser_id, 'elo_rating'].iloc[0]

    # Constants for ELO rating calculation
    K = 32

    # Calculate expected scores
    expected_winner = 1 / (1 + 10**((loser_elo - winner_elo) / 400))
    expected_loser = 1 / (1 + 10**((winner_elo - loser_elo) / 400))

    # Calculate new ELO ratings
    winner_new_elo = winner_elo + int(K * (1 - expected_winner))
    loser_new_elo = loser_elo + int(K * (0 - expected_loser))

    # Update ELO history
    elo_history[winner_id].append(int(winner_new_elo))
    elo_history[loser_id].append(int(loser_new_elo))

    # Update current ELO in study_data
    study_data.loc[study_data['event_ID'] == winner_id, 'elo_rating'] = winner_new_elo
    study_data.loc[study_data['event_ID'] == loser_id, 'elo_rating'] = loser_new_elo

    return winner_new_elo, loser_new_elo

# Update the instability of the event
def update_instability():
    pass

# def get_next_events(study_data, user_answers):
#     window_size = 10
#     next_events = get_next_events_based_on_elo(study_data, window_size)
#     user_pairs = [[a[0], a[1]] for a in user_answers] + [[a[1], a[0]] for a in user_answers]
#     next_event_pairs = [next_events[0]['event_ID'], next_events[1]['event_ID']]

#     c = 0
#     while next_event_pairs in user_pairs:
#         next_events = get_next_events_based_on_elo(study_data, window_size)
#         c += 1
#         if c > window_size * 2:
#             window_size += 10
#             c = 0

#     next_events_dict = {}
#     for i, next_event in enumerate(next_events):
#         next_events_dict[f"event{i}_details"] = str(next_event['event_CLEANED'])
#         next_events_dict[f"event{i}_ID"] = int(next_event['event_ID'])

#     return next_events_dict

def get_next_events(study_data, user_answers):
    window_size = 10
    next_events = get_next_events_based_on_elo(study_data, window_size)
    # Flatten the user_answers list to a set of unique event IDs seen before
    seen_events = set([event_id for pair in user_answers for event_id in pair])
    
    next_event_ids = [next_events[0]['event_ID'], next_events[1]['event_ID']]

    c = 0
    while any(event_id in seen_events for event_id in next_event_ids):
        next_events = get_next_events_based_on_elo(study_data, window_size)
        next_event_ids = [next_events[0]['event_ID'], next_events[1]['event_ID']]
        c += 1
        if c > window_size:
            window_size += 10
            c = 0

    next_events_dict = {}
    for i, next_event in enumerate(next_events):
        next_events_dict[f"event{i}_details"] = str(next_event['event_CLEANED'])
        next_events_dict[f"event{i}_ID"] = int(next_event['event_ID'])

    return next_events_dict


# Returns list of 2 DataFrame rows with event details
def get_next_events_based_on_elo(study_data, window_size=10):
    # First sort the data by elo_rating
    # As optimization this should be changed
    sorted_data = study_data.sort_values(by='elo_rating')

    # Ensure the events are not repeated and their 'seen' counts are balanced
    eligible_events = sorted_data[(sorted_data['seen'] < sorted_data['seen'].mean() + 2) &
                                  (sorted_data['seen'] > sorted_data['seen'].mean() - 2)]

     # Randomly select two events close in elo_rating
    if len(eligible_events) < 2:
        eligible_events = sorted_data  # Fallback to any events if not enough eligible

    # Randomly select the first event
    index1 = random.randint(0, len(eligible_events) - 1)
    
    # Define the range for the second event selection
    lower_bound = max(0, index1 - window_size)
    upper_bound = min(len(eligible_events) - 1, index1 + window_size)

    # Generate a range of indices around the first event
    # This is needed as the lower and upper bounds might be out of the DataFrame index range
    indices = np.arange(lower_bound, upper_bound + 1)

    # Calculate probabilities using Gaussian PDF centered at index1
    mean = index1
    # Standard deviation can be adjusted
    sigma = window_size / 2 
    probabilities = np.exp(-0.5 * ((indices - mean) / sigma) ** 2)
    # Normalize to sum to 1
    probabilities /= probabilities.sum() 

    # Select the second event probabilistically
    # Ensure index2 is not the same as index1
    index2 = np.random.choice(indices, p=probabilities)
    while index1 == index2:
        index2 = np.random.choice(indices, p=probabilities)

    # Update the 'seen' counter for both events
    study_data.at[eligible_events.iloc[index1].name, 'seen'] += 1
    study_data.at[eligible_events.iloc[index2].name, 'seen'] += 1

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