import json
import os

SCORE_FILE = "data/highscores.json"


class HighScoreManager:
    @staticmethod
    def load_high_score() -> int:
        if not os.path.exists(SCORE_FILE):
            return 0
        try:
            with open(SCORE_FILE, "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except Exception:
            return 0

    @staticmethod
    def save_high_score(score: int) -> None:
        os.makedirs(os.path.dirname(SCORE_FILE), exist_ok=True)
        current = HighScoreManager.load_high_score()
        if score > current:
            try:
                with open(SCORE_FILE, "w") as f:
                    json.dump({"high_score": score}, f)
            except Exception as e:
                print(f"Failed to save high score: {e}")
