from utils.data_functions import get_next_events_based_on_elo

class UserProgress:
    def __init__(self, number_of_questions=4, omit_other=True):
        self.number_of_questions = number_of_questions
        self.omit_other = omit_other
        self.user_progress = {}
        self.user_answers = {}
        self.blacklist = []

    def get_next_events(self, user_id, study_data):
        if user_id not in self.user_progress:
            self.user_progress[user_id] = [0, []]

        # Check if the user has completed the study
        if self.user_progress[user_id][0] >= self.number_of_questions:
            return None

        # For now get 2 random even_details from study_data
        next_events = get_next_events_based_on_elo(study_data)

        # Set current events for the user using int(event_ID)s
        self.user_progress[user_id][1] = [int(next_event['event_ID']) for next_event in next_events]

        next_events_dict = {}
        for i, next_event in enumerate(next_events):
            next_events_dict[f"event{i}_details"] = str(next_event['event_details'])
            next_events_dict[f"event{i}_ID"] = int(next_event['event_ID'])

        return next_events_dict

    def submit_answer(self, user_id, loser_id, winner_id, polarity, category=None, classification=None, study_data=None, update_elos=None):
        if user_id not in self.user_progress:
            return {"error": "User ID not found"}

        if user_id in self.blacklist:
            return {"message": "You are no longer a participant"}

        if self.user_progress[user_id][0] >= self.number_of_questions:
            progress = {
                'current_completed': self.user_progress[user_id][0],
                'number_of_questions': self.number_of_questions,
            }
            return {"message": "Study completed", 'progress': progress}

        if not winner_id or not loser_id:
            return {"error": "Answer not provided"}

        if winner_id not in self.user_progress[user_id][1] or loser_id not in self.user_progress[user_id][1]:
            return {"error": "Invalid answer"}

        if not self.omit_other:
            if not category or not classification:
                return {"error": "Category or Classification not provided"}
            study_data.loc[study_data['event_ID'] == winner_id, category] += 1
            study_data.loc[study_data['event_ID'] == winner_id, classification] += 1

        update_elos(winner_id, loser_id, study_data)

        if user_id not in self.user_answers:
            self.user_answers[user_id] = []

        if not self.omit_other:
            self.user_answers[user_id].append([winner_id, loser_id, polarity, category, classification])
        else:
            self.user_answers[user_id].append([winner_id, loser_id, polarity])

        self.user_progress[user_id][0] += 1
        self.user_progress[user_id][1] = []

        progress = {
            'current_completed': self.user_progress[user_id][0],
            'number_of_questions': self.number_of_questions,
        }

        next_events = self.get_next_events(user_id, study_data)
        if not next_events:
            return {"message": "Study completed", 'progress': progress}

        return {'events': next_events, 'progress': progress}

    def block_user(self, user_id):
        self.blacklist.append(user_id)
        return {"message": "You are no longer a participant"}

    def check_user_id(self, user_id):
        if user_id in self.user_progress:
            return {"message": "User ID already exists"}
        return {"message": "User ID is valid", "questions_num": self.number_of_questions}
