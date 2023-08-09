"""
Files API.

This API allows users to create and query for existing data about
files that live in the system.
"""

from fastapi import APIRouter, HTTPException, UploadFile

import use_cases.files as files_use_cases

router = APIRouter(prefix="/files")


@router.get("/")
def list_files():
    return files_use_cases.get_all_file_records()


@router.post("/")
async def upload_file(file: UploadFile):
    content = await file.read()
    size = len(content)
    await file.seek(0)

    with open(file.filename, "wb") as f:
        content = await file.read()
        f.write(content)

    created_record = files_use_cases.create_file_record(file.filename, size)

    return created_record


@router.get("/{file_id}/")
def get_file_details(file_id: str):
    file = files_use_cases.get_file_record_by_id(file_id)

    if file is None:
        return HTTPException(status_code=404)

    return file
