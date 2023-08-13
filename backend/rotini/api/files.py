"""
Files API.

This API allows users to create and query for existing data about
files that live in the system.
"""

import pathlib

from fastapi import APIRouter, HTTPException, UploadFile

import use_cases.files as files_use_cases
from settings import settings

router = APIRouter(prefix="/files")


@router.get("/")
def list_files():
    return files_use_cases.get_all_file_records()


@router.post("/")
async def upload_file(file: UploadFile):
    content = await file.read()
    size = len(content)
    await file.seek(0)

    dest_path = pathlib.Path(settings.STORAGE_ROOT, file.filename)
    with open(dest_path, "wb") as f:
        content = await file.read()
        f.write(content)

    created_record = files_use_cases.create_file_record(str(dest_path), size)

    return created_record


@router.get("/{file_id}/")
def get_file_details(file_id: str):
    file = files_use_cases.get_file_record_by_id(file_id)

    if file is None:
        raise HTTPException(status_code=404)

    return file


@router.delete("/{file_id}/")
def delete_file(file_id: str):
    """
    Deletes a file given its ID.

    This will delete the file in the database records as well
    as on disk. The operation is not reversible.

    DELETE /files/{file_id}/

    200 { <FileData> }
    """
    try:
        file = files_use_cases.delete_file_record_by_id(file_id)
    except files_use_cases.DoesNotExist as exc:
        raise HTTPException(status_code=404) from exc

    return file
