import os, json
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository

class JsonUserRepository(UserRepository):
    def __init__(self, data_dir: str):
        self.file_path = os.path.join(data_dir, "usuarios.json")

    def find_by_email(self, email: str) -> User:
        users = self._load_json()
        for user_data in users:
            if user_data["email"] == email:
                return User(user_data["email"], user_data["password"], user_data["rol"])
        return None

    def _load_json(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r") as f:
            return json.load(f)