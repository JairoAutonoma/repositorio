from domain.repositories.thesis_repository import ThesisRepository

class GetThesesUseCase:
    def __init__(self, thesis_repository: ThesisRepository):
        self.thesis_repository = thesis_repository

    def get_by_author(self, author: str) -> list:
        return self.thesis_repository.find_by_author(author)

    def get_all(self) -> list:
        return self.thesis_repository.find_all()