from typing import Optional
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository

class AuthenticationService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.user_repository.find_by_email(email)
        if user and user.password == password:
            return user
        return None