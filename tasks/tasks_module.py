from fastapi import FastAPI
from .tasks_controller import router

class TasksModule:
    def __init__(self, app: FastAPI):
        app.include_router(router, prefix="/tasks", tags=["tasks"])