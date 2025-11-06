from fastapi import FastAPI
from src.utils.app_logging import setup_logging
from src.controllers import url_controller
from src.utils.settings import settings

setup_logging()
app = FastAPI(title="URL Shortener")

app.include_router(url_controller.router)

@app.get("/")
def root():
    return {"status": "ok"}
