"""
Rotini: a self-hosted cloud storage & productivity app.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import auth.routes as auth_routes
import api.files as files_routes

app = FastAPI()

origins = ["http://localhost:1234"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [files_routes.router, auth_routes.router]

for router in routers:
    app.include_router(router)


@app.get("/", status_code=204)
def healthcheck():
    pass
