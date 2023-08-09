"""
Files API.

This API allows users to create and query for existing data about
files that live in the system.
"""

from fastapi import APIRouter, UploadFile

router = APIRouter(prefix="/files")

data = {
    "123": {
        "title": "Test file",
        "filename": "testfile.txt",
        "size": 1023,
        "uid": "123",
    },
    "456": {
        "title": "Other file",
        "filename": "testfile2.txt",
        "size": 535346,
        "uid": "456",
    },
}


@router.get("/")
def list_files():
    return list(data.values())


@router.post("/")
async def upload_file(file: UploadFile):
    with open(file.filename, "wb") as f:
        content = await file.read()
        f.write(content)
    return file.filename


@router.get("/{file_id}/")
def get_file_details(file_id: str):
    return data[file_id]
