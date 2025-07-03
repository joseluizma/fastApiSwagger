from fastapi import FastAPI
from users.users_controller import router

class UsersModule:
    def __init__(self, app: FastAPI):
        app.include_router(router, prefix="/users", tags=["users"])