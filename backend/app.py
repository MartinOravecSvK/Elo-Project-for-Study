from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.data_functions import get_study_data 

# Create a Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'

# Load the study data as pandas DataFrame
study_data = get_study_data()

# Dictionary to keep track of users and their progress
user_progress = {}

def get_next_questions(user_id):
    if user_id not in user_progress:
        user_progress[user_id] = 0
    current_index = user_progress[user_id]
    next_questions = study_data[current_index:current_index + 2]
    user_progress[user_id] += 2
    return next_questions

@app.route('/next', methods=['GET'])
def get_next_question():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    next_questions = get_next_questions(user_id)
    return jsonify(next_questions)

@app.route('/submit', methods=['POST'])
def submit_answer():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400

    data = request.json.get('answer')
    if not data:
        return jsonify({"error": "Answer not provided"}), 400

    # Handle the submitted answer here
    print(f"Received answer from {user_id}: {data}")

    # Get the next questions
    next_questions = get_next_questions(user_id)
    return jsonify({"status": "success", "next_questions": next_questions}), 200

if __name__ == '__main__':
    app.run(debug=True)
