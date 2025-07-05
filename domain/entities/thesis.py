from typing import Optional
from domain.entities.signature import Signature

class Thesis:
    def __init__(self, id: int, title: str, file: str, author: str, status: str = "En revisión",
                comment: Optional[str] = None, grade: Optional[float] = None, signature: Optional[Signature] = None):
        self.id = id
        self.title = title
        self.file = file
        self.author = author
        self.status = status
        self.comment = comment
        self.grade = grade
        self.signature = signature

    def evaluate(self, comment: str, grade: float):
        self.comment = comment
        self.grade = grade
        self.status = "Evaluada"

    def certify(self, signature: Signature):
        self.signature = signature
        self.status = "Certificada"