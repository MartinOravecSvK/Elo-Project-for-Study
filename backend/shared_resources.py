import threading

class SharedResources:
    user_progress = {}
    user_answers = {}
    blacklist = []
    study_data = None

    user_progress_lock = threading.Lock()
    user_answers_lock = threading.Lock()
    blacklist_lock = threading.Lock()
    study_data_lock = threading.Lock()

    def set_study_data(self, data):
        print("Data Head: ", data.head())
        with self.study_data_lock:
            self.study_data = data
        print("Study Data Head: ", self.study_data.head())