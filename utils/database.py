import logging
import os
import json
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)

    async def initialize(self):
        self.logger.info("DatabaseManager initialized.")

    async def get_user_preferences(self):
        # Placeholder for user preferences
        return {}

    async def save_user_preference(self, key, value):
        # Placeholder for saving user preference
        pass

    async def close(self):
        self.logger.info("DatabaseManager closed.")

    async def store_conversation_history(self, interaction):
        """Store a conversation interaction in a local JSON file."""
        file_path = self.config.get("conversation_history_file", "learning_data/conversation_history.json")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            else:
                history = []
            history.append(interaction)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Error storing conversation history: {e}")

    async def get_conversation_history(self, days=7):
        """Retrieve conversation history from the last N days."""
        file_path = self.config.get("conversation_history_file", "learning_data/conversation_history.json")
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                history = json.load(f)
            cutoff = datetime.now() - timedelta(days=days)
            filtered = [h for h in history if "timestamp" in h and datetime.fromisoformat(h["timestamp"]) >= cutoff]
            return filtered
        except Exception as e:
            self.logger.error(f"Error reading conversation history: {e}")
            return []
