import time
from utils.data_functions import get_study_data, get_user_answers

study_data = get_study_data()
number_of_questions = 20
omit_other = True

# user_answers = {}
user_answers = get_user_answers()
# user_progress = {}
user_progress = {user_id: [len(user_answers[user_id]), [], time.time()] for user_id in user_answers}
blacklist = []
