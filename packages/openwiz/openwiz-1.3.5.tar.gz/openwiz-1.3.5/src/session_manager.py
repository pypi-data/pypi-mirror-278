import json
from src.logger import Logger
import os

class SessionManager:
    def __init__(self, logger: Logger):
        self.logger = logger

    def save_session(self, session_name, prompt, generated_code):
        os.makedirs('sessions', exist_ok=True)
        
        session_data = {
            'prompt': prompt,
            'generated_code': generated_code,
        }
        
        try:
            with open(f"sessions/{session_name}.json", "w") as f:
                json.dump(session_data, f, indent=4)
            self.logger.log(f"> Session '{session_name}' saved.")
        except Exception as e:
            self.logger.log(f"Error saving session '{session_name}': {str(e)}")
            raise

    def load_session(self, session_name):
        with open(f"sessions/{session_name}.json", "r") as f:
            session_data = json.load(f)
        
        generated_code = session_data.get('generated_code', '')
        
        self.logger.log(f"> Session {session_name} loaded")
        return generated_code

    def display_saved_sessions(self):
        sessions_folder = "sessions"
        if not os.path.exists(sessions_folder):
            print("> No sessions found.")
            return
        
        sessions = os.listdir(sessions_folder)
        if not sessions:
            print("> No sessions found.")
            return
        
        print("\nSaved Sessions:\n")
        for index, session_file in enumerate(sessions):
            print(f"{index + 1}. {session_file}")

    def delete_session(self, session_name):
        session_file = f"sessions/{session_name}.json"
        if os.path.exists(session_file):
            os.remove(session_file)
            print(f"\n> Session '{session_name}' deleted.")
        else:
            print(f"\n> Session '{session_name}' not found.")

