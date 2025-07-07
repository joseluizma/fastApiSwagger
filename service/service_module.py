from fastapi import FastAPI
from .service_controller import router

class ServiceModule:
    def __init__(self, app: FastAPI):
        app.include_router(router, prefix="/service", tags=["service"])