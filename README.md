# Elo Study Website

This repository contains the source code for a website designed to conduct a study where participants evaluate and rank events based on their personal opinions. The website allows participants to compare pairs of events and decide which one is either better or worse. The results are then processed using an Elo rating system to rank the events.

## Project Structure

The project is organized into two main parts:

1. **Frontend**: Built using React and JavaScript.
2. **Backend**: Built using Python with Flask.

### Features

- **Event Comparison**: Participants compare pairs of events and choose the one they believe is better or worse.
- **Elo Rating System**: The backend processes the comparison results using an Elo rating system to dynamically rank events.
- **User Progress Tracking**: The application tracks user progress and blocks users who fail attention checks.
- **Data Management**: Handles event data, user answers, and Elo history in a structured manner.

## Installation

### Prerequisites

- Python 3.x (deployed on 3.8)

### Backend Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/elo-study-website.git
cd elo-study-website/backend
```

2. **Create a virtual environment:**

Create a virtual environment that you like, e.g. venv or conda.
Venv: https://docs.python.org/3/library/venv.html
Conda: https://conda.io/projects/conda/en/latest/user-guide/getting-started.html

3. **Install the required Python packages:**

Currently the repository is missing *requirements.txt* so have a look at the code (it's not too big) and intall dependencies as you go. An update will be issued when I have time.

3. **Run the Flask application:**

(in the backend directory)

```bash
python app.py
```

The backend will be available at http://localhost:8000.

## Frontend Setup

The frontend of the application is built using static files (HTML, CSS, and JavaScript). These files are served by the Flask backend directly.

### Deployment

### Prolific Hosting

This project is designed with the intent of hosting on Prolific. The study is integrated with Prolific's platform, and the participant's ID is passed through the URL when the study is launched.

### Environment Variables

- **Backend**: Ensure that sensitive information such as the secret key and database connection strings are stored securely using environment variables.

## Usage

### Starting the Study

When a participant begins the study, they will go through several instruction pages before starting the main event comparison task. The results of their comparisons will be used to adjust the Elo ratings of the events.

### Completion and Redirect

Upon completing the study, participants will be redirected to Prolific using a unique completion code.

### Data Storage

The outputs of the study are stored in the `output` directory within the backend. The data includes:

- **User Answers**: Stored in `output/user_answers.json`.
- **Study Data**: Stored in `output/study_data.json`.
- **Elo History**: Stored in `output/elo_history.json`.

The data is saved using the following method:
```python
def save_data():
    user_answers_file = 'output/user_answers.json'
    with user_answers_lock:
        with open(user_answers_file, 'w') as f:
            json.dump(user_answers, f)
    study_data_file = 'output/study_data.json'
    with study_data_lock:
        with open(study_data_file, 'w') as f:
            json.dump(study_data.to_dict(orient='records'), f, default=custom_encoder)
        with open('output/elo_history.json', 'w') as f:
            json.dump(elo_history, f)
```

### Elo Rating Calculation
The Elo rating for each event is calculated using the following formula:

## Elo Rating Calculation

The Elo rating for each event is updated based on the following formulas:

## Elo Rating Calculation

The Elo rating for each event is updated based on the following steps:

1. **Expected Score Calculation**:

   - Expected score for the winner: `E_w = 1 / (1 + 10^((R_l - R_w) / 400))`
   - Expected score for the loser: `E_l = 1 / (1 + 10^((R_w - R_l) / 400))`

   where:
   - `R_w` is the current Elo rating of the winner.
   - `R_l` is the current Elo rating of the loser.

2. **New Elo Rating Calculation**:

   - New rating for the winner: `R'_w = R_w + K * (1 - E_w)`
   - New rating for the loser: `R'_l = R_l + K * (0 - E_l)`

   where:
   - `K` is a constant (often set to 32) that determines the sensitivity of the rating system.
   - `1` represents the actual score for the winner.
   - `0` represents the actual score for the loser.

