from domain.entities.thesis import Thesis
from domain.entities.signature import Signature
from domain.repositories.thesis_repository import ThesisRepository

class ThesisService:
    def __init__(self, thesis_repository: ThesisRepository):
        self.thesis_repository = thesis_repository

    def upload_thesis(self, title: str, file: str, author: str) -> Thesis:
        thesis_id = self.thesis_repository.get_next_id()
        thesis = Thesis(id=thesis_id, title=title, file=file, author=author)
        self.thesis_repository.save(thesis)
        return thesis

    def evaluate_thesis(self, thesis_id: int, comment: str, grade: float):
        theses = self.thesis_repository.find_all()
        for thesis in theses:
            if thesis.id == thesis_id:
                thesis.evaluate(comment, grade)
                self.thesis_repository.save(thesis)
                return
        raise ValueError("Tesis no encontrada")

    def certify_thesis(self, thesis_id: int, signed_by: str):
        theses = self.thesis_repository.find_all()
        for thesis in theses:
            if thesis.id == thesis_id:
                signature = Signature.create(signed_by, thesis_id)
                thesis.certify(signature)
                self.thesis_repository.save(thesis)
                return
        raise ValueError("Tesis no encontrada")