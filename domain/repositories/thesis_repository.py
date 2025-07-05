from abc import ABC, abstractmethod
from typing import List
from domain.entities.thesis import Thesis

class ThesisRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[Thesis]:
        pass

    @abstractmethod
    def find_by_author(self, author: str) -> List[Thesis]:
        pass

    @abstractmethod
    def save(self, thesis: Thesis):
        pass

    @abstractmethod
    def get_next_id(self) -> int:
        pass