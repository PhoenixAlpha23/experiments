# server.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os, shutil

app = FastAPI()
STORAGE_DIR = "D:\\Code\\sharedd"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    dest = os.path.join(STORAGE_DIR, file.filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"status": "uploaded", "file": file.filename}

@app.get("/files")
def list_files():
    return os.listdir(STORAGE_DIR)

@app.get("/download/{filename}")
def download(filename: str):
    path = os.path.join(STORAGE_DIR, filename)
    return FileResponse(path, filename=filename)
