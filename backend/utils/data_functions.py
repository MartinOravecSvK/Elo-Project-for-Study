from pandas import read_excel
from os import path

# Columns to drop from the study data                          
# 'event_valence' might be useful for better ELO rating calculation
DROP_COLUMNS = ['fileName', 'study_number', 'participant_ID', 'event_valence', 'event_when', 'event_known']

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
    # Adding 950 centers the ELO rating to 1000 (might not be the best approach, but it's a simple one for this example) 
    study_data['elo_rating'] = 950 + study_data['slider_end']

    # Finally drop the slider_end column
    study_data.drop(columns=['slider_end'], inplace=True)
    
    return study_data

# Just a simple function to update the ELO ratings
def update_elos(winner_elo, loser_elo):
    # Constants for the ELO rating calculation (Try to experiment with these values)
    K = 32
    E = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))

    # Calculate the new ELO ratings
    winner_new_elo = winner_elo + K * (1 - E)
    loser_new_elo = loser_elo + K * (0 - E)

    return winner_new_elo, loser_new_elo

if __name__ == '__main__':
    # Load the study data
    study_data = get_study_data()

    # Print the study data columns
    print(study_data.columns)
    print(study_data.head())