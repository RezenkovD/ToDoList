from fastapi import FastAPI

from src.routes.task import router

app = FastAPI()

app.include_router(router)
