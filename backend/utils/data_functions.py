from pandas import read_excel
from os import path
import random
import numpy as np

# Columns to drop from the study data                          
# 'event_valence' might be useful for better ELO rating calculation
DROP_COLUMNS = ['fileName', 'study_number', 'participant_ID', 'event_valence', 'event_when', 'event_known']

# Additional columns for the study data (all just counters)
categories = ['Health', 'Financial', 'Relationship', 'Bereavement', 'Work', 'Crime']
classification = ['Daily', 'Major']

# Returns the study data as a pandas DataFrame
# Columns: ['event_details', 'event_ID', 'elo_rating']
def get_study_data():
    # Get the study data path
    current_dir = path.dirname(path.abspath(__file__))
    study_data_path = path.join(current_dir, '../data/All_Studies_SigEvent_details.xlsx')

    # Load the study data
    study_data = read_excel(study_data_path)
    study_data.drop(columns=DROP_COLUMNS, inplace=True)

    # Initialize ELO rating for each sentence based on the slider_end column ((doesn't make sense)0 - (makes complete sense)100)
    slider_factor = 2.5
    study_data['elo_rating'] = (1000 - 50 * slider_factor) + study_data['slider_end'] * slider_factor

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

# Just a simple function to update the ELO ratings
def update_elos(winner_elo, loser_elo):
    # Constants for the ELO rating calculation (Try to experiment with these values)
    K = 32
    E = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))

    # Calculate the new ELO ratings
    winner_new_elo = winner_elo + K * (1 - E)
    loser_new_elo = loser_elo + K * (0 - E)

    return int(winner_new_elo), int(loser_new_elo)

# Update the confidence of the event
def update_confidence():
    pass

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