from pydantic import BaseModel
from typing import List

class UploadResponse(BaseModel):
    status: str
    file: str

class FileListResponse(BaseModel):
    files: List[str]