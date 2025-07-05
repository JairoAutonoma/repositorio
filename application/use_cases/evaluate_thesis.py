from domain.services.thesis_service import ThesisService

class EvaluateThesisUseCase:
    def __init__(self, thesis_service: ThesisService):
        self.thesis_service = thesis_service

    def execute(self, thesis_id: int, comment: str, grade: float) -> dict:
        self.thesis_service.evaluate_thesis(thesis_id, comment, grade)
        return {"msg": "Tesis evaluada"}