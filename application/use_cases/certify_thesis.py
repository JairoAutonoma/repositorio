from domain.services.thesis_service import ThesisService

class CertifyThesisUseCase:
    def __init__(self, thesis_service: ThesisService):
        self.thesis_service = thesis_service

    def execute(self, thesis_id: int, signed_by: str) -> dict:
        self.thesis_service.certify_thesis(thesis_id, signed_by)
        return {"msg": "Tesis certificada con firma electrónica"}