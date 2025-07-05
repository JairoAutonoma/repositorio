from domain.services.thesis_service import ThesisService

class UploadThesisUseCase:
    def __init__(self, thesis_service: ThesisService):
        self.thesis_service = thesis_service

    def execute(self, title: str, file: str, author: str) -> dict:
        thesis = self.thesis_service.upload_thesis(title, file, author)
        return {"msg": "Tesis subida correctamente"}