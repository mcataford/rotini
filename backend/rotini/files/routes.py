"""
Files API.

This API allows users to create and query for existing data about
files that live in the system.
"""

import pathlib

from fastapi import APIRouter, HTTPException, UploadFile, Request
from fastapi.responses import FileResponse

import files.use_cases as files_use_cases
from settings import settings

router = APIRouter(prefix="/files")


@router.get("/", status_code=200)
async def list_files(request: Request):
    """
    Fetches all files owned by the logged-in user.

    200 { [<FileRecord>, ...] }

        If the user is logged in, file records that they
        own are returned.

    401 {}

        If the request is not authenticated, it fails.
    """
    # FIXME: Temporarily fetching files belonging to the base user.
    #   to be resolved once users can log in.
    current_user_id = (
        request.state.user["user_id"] if hasattr(request.state, "user") else 1
    )
    return files_use_cases.get_all_files_owned_by_user(current_user_id)


@router.post("/", status_code=201)
async def upload_file(request: Request, file: UploadFile) -> files_use_cases.FileRecord:
    """
    Receives files uploaded by the user, saving them to disk and
    recording their existence in the database.

    201 { <FileRecord> }

        The file was uploaded and registered successfully.
    """

    content = await file.read()
    size = len(content)
    dest_path = pathlib.Path(settings.STORAGE_ROOT, file.filename)

    with open(dest_path, "wb") as f:
        f.write(content)
    # FIXME: Temporarily fetching files belonging to the base user.
    #   to be resolved once users can log in.
    created_record = files_use_cases.create_file_record(
        str(dest_path),
        size,
        request.state.user["user_id"] if hasattr(request.state, "user") else 1,
    )

    return created_record


@router.get("/{file_id}/")
def get_file_details(file_id: str):
    file = files_use_cases.get_file_record_by_id(file_id)

    if file is None:
        raise HTTPException(status_code=404)

    return file


@router.get("/{file_id}/content/")
def get_file_content(file_id: str) -> FileResponse:
    """
    Retrieves the file data associated with a given File ID.

    This returns the file for download as a streamed file.

    GET /files/{file_id}/content/

    200 { <File> }

        The file data is returned as a stream if the file exists.

    404 {}

        The file ID did not map to anything.
    """
    file = files_use_cases.get_file_record_by_id(file_id)

    if file is None:
        raise HTTPException(status_code=404)

    return FileResponse(
        path=file["path"],
        media_type="application/octet-stream",
        filename=file["filename"],
    )


@router.delete("/{file_id}/")
def delete_file(file_id: str) -> files_use_cases.FileRecord:
    """
    Deletes a file given its ID.

    This will delete the file in the database records as well
    as on disk. The operation is not reversible.

    DELETE /files/{file_id}/

    200 { <FileRecord> }

        The file exists and has been deleted from storage and
        from the database.

    404 {}

        The file ID did not map to anything.

    """
    try:
        file = files_use_cases.delete_file_record_by_id(file_id)
    except files_use_cases.DoesNotExist as exc:
        raise HTTPException(status_code=404) from exc

    return file
