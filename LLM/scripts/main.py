import pandas as pd
import random
import numpy as np
from tqdm import tqdm
from chatgpt.chatgpt_run import run_chatgpt
from collections import defaultdict
from pandas import read_excel

events_file = "./data/dataset/All_Studies_SigEvent_details_CLEANED_23.05.2024.xlsx"

prompt_intro = """
You are invited to take part in a research study to compare statements about life experiences.

What is this study about?

The purpose of this study is to better understand judgments of life experiences. The life experience statements used in this study vary widely. Some statements may refer to everyday occurrences (e.g., losing an item); other statements may refer to more impactful life events (e.g., loss of a loved one). By asking you to compare these differing types of statements, we aim to understand how you rank various life experiences.

What will you have to do?

You will be asked to compare multiple pairs of statements that refer to life experiences. You will have to decide which of the statements is comparatively better or worse than the other, depending on the phrasing of the question when these statements are presented to you. The events are provided without context, so you can be as general as you wish.

Please respond with only '1' or '2' without any additional text.
"""

window_size = 10

DROP_COLUMNS = ['fileName', 'study_number', 'participant_ID', 'event_valence', 'event_when', 'event_known', 'Use?', 'event_details']

def load_study_data():
    study_data = read_excel(events_file, engine='openpyxl')
    study_data = study_data[study_data['Use?'] == 'Yes']
    study_data.drop(columns=DROP_COLUMNS, inplace=True)

    slider_factor = 2.5
    initial_elo = ((1000 - 50 * slider_factor) + study_data['slider_end'] * slider_factor).astype(int)
    study_data['elo_rating'] = initial_elo
    study_data['seen'] = 0
    study_data.drop(columns=['slider_end'], inplace=True)

    return study_data

decisions = defaultdict(list)

def update_elos(study_data, winner, loser, model):
    K = 32

    winner_elo = study_data.loc[study_data['event_ID'] == winner['event_ID'], 'elo_rating'].values[0]
    loser_elo = study_data.loc[study_data['event_ID'] == loser['event_ID'], 'elo_rating'].values[0]

    expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    expected_loser = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))

    winner_new_elo = winner_elo + int(K * (1 - expected_winner))
    loser_new_elo = loser_elo + int(K * (0 - expected_loser))

    study_data.loc[study_data['event_ID'] == winner['event_ID'], 'elo_rating'] = winner_new_elo
    study_data.loc[study_data['event_ID'] == loser['event_ID'], 'elo_rating'] = loser_new_elo

    study_data.loc[study_data['event_ID'] == winner['event_ID'], 'seen'] += 1
    study_data.loc[study_data['event_ID'] == loser['event_ID'], 'seen'] += 1

    decisions[model].append({
        'winner': winner['event_ID'],
        'loser': loser['event_ID'],
        'winner_elo': winner_elo,
        'loser_elo': loser_elo,
        'winner_new_elo': winner_new_elo,
        'loser_new_elo': loser_new_elo
    })

def choose_events(study_data):
    # Sort study_data by elo_rating
    study_data.sort_values(by='elo_rating', inplace=True, ascending=False)
    study_data.reset_index(drop=True, inplace=True)

    eligible_events = study_data[study_data['seen'] <= study_data['seen'].mean()]
    
    if len(eligible_events) < 2:
        eligible_events = study_data

    index1 = random.randint(0, len(eligible_events) - 1)

    lower_bound = max(0, index1 - window_size)
    upper_bound = min(len(eligible_events) - 1, index1 + window_size)
    
    indices = np.arange(lower_bound, upper_bound + 1)

    # Calculate probabilities using Gaussian PDF centered at index1
    mean = index1
    sigma = window_size / 2  # Standard deviation can be adjusted
    probabilities = np.exp(-0.5 * ((indices - mean) / sigma) ** 2)
    probabilities /= probabilities.sum()

    index2 = np.random.choice(indices, p=probabilities)
    while index1 == index2:
        index2 = np.random.choice(indices, p=probabilities)

    event1 = eligible_events.iloc[index1]
    event2 = eligible_events.iloc[index2]

    return event1, event2

def run_comparison_chatGPT(study_data, prompt_intro, comparisons, model):
    conversation_history = [
        {"role": "system", "content": prompt_intro.strip()}
    ]

    for _ in range(comparisons):
        event1, event2 = choose_events(study_data)
        # print(f"\nComparing:\n1. {event1['event_CLEANED']}\n2. {event2['event_CLEANED']}")

        choosing_better = random.random() < 0.5

        if choosing_better:
            question = f"Which of the following life experiences is comparatively better?\n1. {event1['event_CLEANED']}\n2. {event2['event_CLEANED']}\nPlease respond with only '1' or '2' without any additional text."
        else:
            question = f"Which of the following life experiences is comparatively worse?\n1. {event1['event_CLEANED']}\n2. {event2['event_CLEANED']}\nPlease respond with only '1' or '2' without any additional text."

        conversation_history.append({"role": "user", "content": question.strip()})

        response = run_chatgpt(conversation_history, model)
        
        if response is None:
            print("No response received. Skipping this comparison.")
            continue

        if response == "1":
            if choosing_better:
                update_elos(study_data, event1, event2, model)
            else:
                update_elos(study_data, event2, event1, model)
        elif response == "2":
            if choosing_better:
                update_elos(study_data, event2, event1, model)
            else:
                update_elos(study_data, event1, event2, model)
        else:
            print("Invalid response received:", response)

        # Add the model's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response.strip()})


def save_results(study_data, model):
    # Save per model data
    df = pd.DataFrame(decisions[model])
    df.to_csv(f'./data/output/{model}_results.csv', index=False)
    # Save study_data
    study_data.to_csv(f'./data/output/{model}_study_data.csv', index=False)
    print(f"Results saved for model {model}")

if __name__ == "__main__":
    # chatGPT_models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
    chatGPT_models = ["gpt-4-turbo"]
    comparisons = 50
    sim_participants = 35
    # 105 left
    for model in chatGPT_models:
        for _ in tqdm(range(sim_participants)):
            study_data = load_study_data()
            # print(f"\nRunning {comparisons} comparisons for {model}")
            run_comparison_chatGPT(study_data, prompt_intro, comparisons, model)
            save_results(study_data, model)
    print("Done!")
