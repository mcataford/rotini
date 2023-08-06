from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:1234"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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


@app.get("/", status_code=204)
def healthcheck():
    pass


@app.get("/files/")
def list_files():
    return list(data.values())


@app.get("/files/{fileId}/")
def get_file_details(fileId: str):
    return data[fileId]
