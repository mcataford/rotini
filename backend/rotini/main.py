"""
Rotini: a self-hosted cloud storage & productivity app.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import api.users
import api.files

app = FastAPI()

origins = ["http://localhost:1234"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.files.router)
app.include_router(api.users.router)


@app.get("/", status_code=204)
def healthcheck():
    pass
