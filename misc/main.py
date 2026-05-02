from fastapi import FastAPI
import logging
from app.api.routes import router

app = FastAPI(title="File Share API")

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

app.include_router(router)