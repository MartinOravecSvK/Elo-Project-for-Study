import threading

user_progress_lock = threading.Lock()
user_answers_lock = threading.Lock()
blacklist_lock = threading.Lock()
study_data_lock = threading.Lock()
