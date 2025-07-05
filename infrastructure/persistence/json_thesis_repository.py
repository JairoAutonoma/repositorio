import os, json
from typing import List
from domain.entities.thesis import Thesis
from domain.entities.signature import Signature
from domain.repositories.thesis_repository import ThesisRepository

class JsonThesisRepository(ThesisRepository):
    def __init__(self, data_dir: str):
        self.file_path = os.path.join(data_dir, "tesis.json")

    def find_all(self) -> List[Thesis]:
        data = self._load_json()
        return [self._to_entity(t) for t in data]

    def find_by_author(self, author: str) -> List[Thesis]:
        data = self._load_json()
        return [self._to_entity(t) for t in data if t["autor"] == author]

    def save(self, thesis: Thesis):
        theses = self._load_json()
        thesis_data = {
            "id": thesis.id,
            "titulo": thesis.title,
            "archivo": thesis.file,
            "autor": thesis.author,
            "estado": thesis.status,
            "comentario": thesis.comment,
            "nota": thesis.grade,
            "firma": {
                "firmado_por": thesis.signature.signed_by,
                "fecha": thesis.signature.date,
                "hash": thesis.signature.hash
            } if thesis.signature else None
        }
        for i, t in enumerate(theses):
            if t["id"] == thesis.id:
                theses[i] = thesis_data
                break
        else:
            theses.append(thesis_data)
        self._save_json(theses)

    def get_next_id(self) -> int:
        theses = self._load_json()
        return max([t["id"] for t in theses], default=0) + 1

    def _load_json(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _save_json(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)

    def _to_entity(self, data: dict) -> Thesis:
        signature = None
        if data.get("firma"):
            signature = Signature(
                signed_by=data["firma"]["firmado_por"],
                date=data["firma"]["fecha"],
                hash=data["firma"]["hash"]
            )
        return Thesis(
            id=data["id"],
            title=data["titulo"],
            file=data["archivo"],
            author=data["autor"],
            status=data["estado"],
            comment=data.get("comentario"),
            grade=data.get("nota"),
            signature=signature
        )