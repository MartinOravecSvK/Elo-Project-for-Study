import sqlite3
from flask import g
import pandas as pd
import json
from os import path
from pandas import read_excel

DATABASE = 'study_data.db'

# Columns to drop from the study data                          
DROP_COLUMNS = ['fileName', 'study_number', 'participant_ID', 'event_valence', 'event_when', 'event_known', 'Use?', 'event_details']

# Additional columns for the study data (all just counters)
categories = ['Health', 'Financial', 'Relationship', 'Bereavement', 'Work', 'Crime']
classification = ['Daily', 'Major']

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, timeout=10, check_same_thread=False)
        db.execute('PRAGMA journal_mode=WAL;')  # Enable WAL mode for better concurrency
    return db

def init_db():
    with sqlite3.connect(DATABASE, timeout=10, check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                user_id TEXT PRIMARY KEY,
                progress INTEGER,
                event1_id INTEGER,
                event2_id INTEGER,
                timestamp REAL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS user_answers (
                user_id TEXT,
                winner_id INTEGER,
                loser_id INTEGER,
                polarity TEXT,
                category TEXT,
                classification TEXT,
                delta_time REAL,
                PRIMARY KEY (user_id, winner_id, loser_id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS blacklist (
                user_id TEXT PRIMARY KEY
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS study_data (
                event_ID INTEGER PRIMARY KEY,
                event_CLEANED TEXT,
                elo_rating INTEGER,
                seen INTEGER,
                instability INTEGER,
                Health INTEGER,
                Financial INTEGER,
                Relationship INTEGER,
                Bereavement INTEGER,
                Work INTEGER,
                Crime INTEGER,
                Daily INTEGER,
                Major INTEGER
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS elo_history (
                event_ID INTEGER PRIMARY KEY,
                history TEXT  -- JSON string of ELO ratings over time
            )
        ''')

        # Initialize data in study_data and elo_history tables
        initialize_study_data(conn)

def initialize_study_data(conn):
    c = conn.cursor()
    # Check if study_data table is empty
    c.execute('SELECT COUNT(*) FROM study_data')
    if c.fetchone()[0] > 0:
        print('Study data already initialized')
        return

    # Load study data from JSON file or Excel file
    study_data = load_study_data()

    # Insert study_data into the database
    study_data.to_sql('study_data', conn, if_exists='append', index=False)

    # Initialize elo_history table
    c.execute('SELECT COUNT(*) FROM elo_history')
    if c.fetchone()[0] == 0:
        initialize_elo_history(conn, study_data)

    conn.commit()

def load_study_data():
    study_data_file = 'output/study_data.json'
    if path.exists(study_data_file):
        print('Loading study data from JSON file')
        study_data = pd.read_json(study_data_file, orient='split')
        study_data['seen'] = 0  # Reset 'seen' counts
    else:   
        print('Loading study data from Excel file')
        current_dir = path.dirname(path.abspath(__file__))
        study_data_path = path.join(current_dir, 'data/All_Studies_SigEvent_details_CLEANED_23.05.2024.xlsx')

        # Load the study data
        study_data = read_excel(study_data_path, engine='openpyxl')

        # Use only rows with Use? set to Yes
        study_data = study_data[study_data['Use?'] == 'Yes']

        # Drop the unnecessary columns
        study_data.drop(columns=DROP_COLUMNS, inplace=True)

        # Initialize ELO rating for each event
        slider_factor = 2.5
        initial_elo = ((1000 - 50 * slider_factor) + study_data['slider_end'] * slider_factor).astype(int)
        study_data['elo_rating'] = initial_elo

        # Add 'seen' and 'instability' columns
        study_data['seen'] = 0
        study_data['instability'] = 0

        # Drop the 'slider_end' column
        study_data.drop(columns=['slider_end'], inplace=True)

        # Add category and classification columns
        for col in categories + classification:
            study_data[col] = 0

    return study_data

def initialize_elo_history(conn, study_data):
    c = conn.cursor()
    elo_history_file = 'output/elo_history.json'
    if path.exists(elo_history_file):
        print('Loading ELO history from JSON file')
        with open(elo_history_file, 'r') as f:
            elo_history = json.load(f)
    else:
        print('Initializing ELO history')
        elo_history = {str(row['event_ID']): [row['elo_rating']] for _, row in study_data.iterrows()}

    # Insert elo_history into the database
    for event_ID_str, history_list in elo_history.items():
        event_ID = int(event_ID_str)
        history_json = json.dumps(history_list)
        c.execute('INSERT INTO elo_history (event_ID, history) VALUES (?, ?)', (event_ID, history_json))

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
