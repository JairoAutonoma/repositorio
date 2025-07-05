import os

class FileStorage:
    def __init__(self, pdf_dir: str):
        self.pdf_dir = pdf_dir
        os.makedirs(self.pdf_dir, exist_ok=True)

    def save_file(self, file, filename: str):
        path = os.path.join(self.pdf_dir, filename)
        file.save(path)
        return path

    def get_file_path(self, filename: str) -> str:
        return os.path.join(self.pdf_dir, filename)