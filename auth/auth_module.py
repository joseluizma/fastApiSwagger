from fastapi import FastAPI
from .auth_controller import router

class AuthModule:
    def __init__(self, app: FastAPI):
        app.include_router(router, prefix="/auth", tags=["auth"])