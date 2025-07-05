from dataclasses import dataclass
from hashlib import sha256
from datetime import datetime

@dataclass
class Signature:
    signed_by: str
    date: str
    hash: str

    @staticmethod
    def create(signed_by: str, thesis_id: int) -> 'Signature':
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hash_value = sha256(f"{thesis_id}{signed_by}{datetime.now()}".encode()).hexdigest()[:10]
        return Signature(signed_by, date, hash_value)