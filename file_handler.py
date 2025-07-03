

import os
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_file(file, file_id):
    path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    with open(path, "wb") as f:
        f.write(file.file.read())
    return str(path)

def get_file_by_id(file_id: str):
    for file in os.listdir(UPLOAD_DIR):
        if file.startswith(file_id):
            return {"id": file_id, "name": file.split('_', 1)[1], "path": str(UPLOAD_DIR / file)}
    return None
